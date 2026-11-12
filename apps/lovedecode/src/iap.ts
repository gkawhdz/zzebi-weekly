import { IAP, Storage, type CompletedOrRefundedOrdersResult } from '@apps-in-toss/web-framework';

// ▼ 앱인토스 콘솔 > 수익화 > 인앱 결제에서 '비소모성(한 번 사면 평생)' 상품을 만들고
//   발급된 상품 SKU를 여기에 넣어주세요. 비어 있으면 결제 버튼이 안내 문구만 보여줘요.
export const PRODUCT_SKU = '';

const KEY = 'lovedecode_unlocked_v1';

async function saveUnlocked() {
  try {
    await Storage.setItem(KEY, '1');
  } catch {
    try {
      localStorage.setItem(KEY, '1');
    } catch {
      /* 저장 실패해도 주문 내역으로 복원 가능 */
    }
  }
}

async function readCached(): Promise<boolean> {
  try {
    if ((await Storage.getItem(KEY)) === '1') return true;
  } catch {
    /* 토스 밖 환경 */
  }
  try {
    return localStorage.getItem(KEY) === '1';
  } catch {
    return false;
  }
}

export function iapSupported() {
  try {
    return !!PRODUCT_SKU && IAP.createOneTimePurchaseOrder.isSupported();
  } catch {
    return false;
  }
}

/** 결제 완료됐지만 지급이 안 된 주문을 마저 처리해요 */
async function grantPending(): Promise<boolean> {
  try {
    if (!IAP.getPendingOrders.isSupported()) return false;
    const { orders } = await IAP.getPendingOrders();
    let granted = false;
    for (const o of orders) {
      if (o.sku !== PRODUCT_SKU) continue;
      await saveUnlocked();
      try {
        if (IAP.completeProductGrant.isSupported()) {
          await IAP.completeProductGrant({ params: { orderId: o.orderId } });
        }
      } catch {
        /* 다음 실행 때 다시 시도 */
      }
      granted = true;
    }
    return granted;
  } catch {
    return false;
  }
}

/** 주문 내역에서 구매 여부를 확인해요 (기기 변경·재설치 복원) */
async function fromOrderHistory(): Promise<boolean> {
  try {
    if (!IAP.getCompletedOrRefundedOrders.isSupported()) return false;
    let key: string | null | undefined = null;
    let owned = false;
    for (let i = 0; i < 10; i++) {
      const res: CompletedOrRefundedOrdersResult = await IAP.getCompletedOrRefundedOrders({ key });
      for (const o of res.orders) {
        if (o.sku !== PRODUCT_SKU) continue;
        owned = o.status === 'COMPLETED';
      }
      if (!res.hasNext) break;
      key = res.nextKey;
    }
    if (owned) await saveUnlocked();
    return owned;
  } catch {
    return false;
  }
}

export async function checkUnlocked(): Promise<boolean> {
  if (await readCached()) return true;
  if (!PRODUCT_SKU) return false;
  if (await grantPending()) return true;
  return fromOrderHistory();
}

export async function restorePurchase(): Promise<boolean> {
  if (!PRODUCT_SKU) return false;
  if (await grantPending()) return true;
  return fromOrderHistory();
}

export function purchase(onDone: (ok: boolean, message?: string) => void) {
  if (!iapSupported()) {
    onDone(false, PRODUCT_SKU ? '토스 앱을 최신 버전으로 업데이트해 주세요' : '결제 준비 중이에요');
    return;
  }
  let cleanup: (() => void) | undefined;
  const finish = (ok: boolean, msg?: string) => {
    try {
      cleanup?.();
    } catch {
      /* noop */
    }
    onDone(ok, msg);
  };
  try {
    cleanup = IAP.createOneTimePurchaseOrder({
      options: {
        sku: PRODUCT_SKU,
        processProductGrant: async () => {
          await saveUnlocked();
          return true;
        },
      },
      onEvent: (e) => {
        if (e.type === 'success') finish(true);
      },
      onError: (err) => {
        const code = (err as { code?: string })?.code;
        if (code === 'USER_CANCELED') finish(false);
        else if (code === 'ITEM_ALREADY_OWNED') {
          void saveUnlocked().then(() => finish(true));
        } else finish(false, '결제를 완료하지 못했어요. 잠시 후 다시 시도해 주세요');
      },
    });
  } catch {
    finish(false, '결제를 시작하지 못했어요');
  }
}
