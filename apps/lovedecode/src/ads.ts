import { loadFullScreenAd, showFullScreenAd } from '@apps-in-toss/web-framework';

// ▼ 앱인토스 콘솔 > 수익화 > 인앱 광고에서 '전면형' 광고 그룹을 만든 뒤
//   발급받은 광고 그룹 ID를 여기에 넣어주세요. 비어 있으면 광고 없이 동작해요.
export const AD_GROUP_ID = 'ait.v2.live.afac30ee3817479a';

let loaded = false;

function supported() {
  try {
    return !!AD_GROUP_ID && loadFullScreenAd.isSupported() && showFullScreenAd.isSupported();
  } catch {
    return false;
  }
}

/** 테스트 시작할 때 미리 광고를 불러와 둬요. */
export function preloadAd() {
  if (!supported()) return;
  loaded = false;
  try {
    loadFullScreenAd({
      options: { adGroupId: AD_GROUP_ID },
      onEvent: (e) => {
        if (e.type === 'loaded') loaded = true;
      },
      onError: () => {
        loaded = false;
      },
    });
  } catch {
    loaded = false;
  }
}

/** 결과 보기 전에 광고를 보여줘요. 광고가 없거나 실패해도 결과는 항상 보여줘요. */
export function showAdThen(done: () => void) {
  if (!supported() || !loaded) {
    done();
    return;
  }
  let finished = false;
  const finish = () => {
    if (finished) return;
    finished = true;
    loaded = false;
    done();
  };
  // 광고가 응답하지 않을 때를 대비한 안전장치
  const timer = setTimeout(finish, 15000);
  try {
    showFullScreenAd({
      options: { adGroupId: AD_GROUP_ID },
      onEvent: (e) => {
        if (e.type === 'dismissed' || e.type === 'failedToShow') {
          clearTimeout(timer);
          finish();
        }
      },
      onError: () => {
        clearTimeout(timer);
        finish();
      },
    });
  } catch {
    clearTimeout(timer);
    finish();
  }
}

/** 지금 광고를 보여줄 수 있는지 (안내 화면을 띄울지 판단할 때 써요) */
export function adReady() {
  return supported() && loaded;
}
