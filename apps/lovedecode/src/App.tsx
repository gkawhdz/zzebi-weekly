import { useEffect, useMemo, useRef, useState } from 'react';
import { Share } from '@apps-in-toss/web-framework';
import {
  ADVICE,
  POSTS,
  FREE_COUNT,
  SLIDES_PER_POST,
  QUESTIONS,
  SCALE,
  DOMAIN_LABEL,
  HEALTH_DOMAINS,
  computeScores,
  health,
  weakest,
} from './data';
import { preloadAd, showAdThen, adReady } from './ads';
import { checkUnlocked, purchase, restorePurchase } from './iap';
import './App.css';

const slideSrc = (ep: string, n: number) => `./posts/${ep}/slide_${String(n).padStart(2, '0')}.jpg`;

const SIGNS = Object.entries(ADVICE).map(([k, v]) => ({ key: k, ...v }));
const SIGN_LABEL: Record<string, string> = {
  respect: '존중',
  conflict: '싸움 뒤 회복',
  trust: '신뢰',
  warmth: '마음의 온도',
  balance: '주고받기 균형',
  future: '함께 그리는 미래',
};

export default function App() {
  const [unlocked, setUnlocked] = useState(false);
  const [viewer, setViewer] = useState<string | null>(null);
  const [guide, setGuide] = useState(false);
  const [check, setCheck] = useState(false);
  const [paywall, setPaywall] = useState(false);
  const [toast, setToast] = useState('');
  const opens = useRef(0);
  const [adGate, setAdGate] = useState<null | (() => void)>(null);

  useEffect(() => {
    void checkUnlocked().then(setUnlocked);
    preloadAd();
  }, []);

  // 화면(글 보기·점검·안내)을 열 때 기록을 남겨서, 토스 상단바 뒤로가기로 닫혀요.
  const overlayOpen = !!(viewer || guide || check || paywall || adGate);
  const pushed = useRef(false);
  useEffect(() => {
    if (overlayOpen && !pushed.current) {
      try {
        history.pushState({ overlay: 1 }, '');
        pushed.current = true;
      } catch {
        /* */
      }
    }
    if (!overlayOpen) pushed.current = false;
  }, [overlayOpen]);
  useEffect(() => {
    const onPop = () => {
      pushed.current = false;
      setViewer(null);
      setGuide(false);
      setCheck(false);
      setPaywall(false);
      setAdGate(null);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);
  const closeOverlay = () => {
    if (pushed.current) history.back();
    else {
      setViewer(null);
      setGuide(false);
      setCheck(false);
      setPaywall(false);
      setAdGate(null);
    }
  };
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(''), 2200);
    return () => clearTimeout(t);
  }, [toast]);

  // 구매하지 않은 사용자는 콘텐츠를 두 번 열 때마다 한 번, 안내 화면을 거쳐 광고가 나와요
  const withAd = (open: () => void) => {
    if (unlocked) return open();
    opens.current += 1;
    if (opens.current % 2 === 1 && adReady()) setAdGate(() => open);
    else open();
  };
  const watchAdThenOpen = () => {
    const open = adGate;
    setAdGate(null);
    showAdThen(() => {
      open?.();
      preloadAd();
    });
  };

  const openPost = (ep: string, i: number) => {
    if (i < FREE_COUNT || unlocked) withAd(() => setViewer(ep));
    else setPaywall(true);
  };

  const buy = () =>
    purchase((ok, msg) => {
      if (ok) {
        setUnlocked(true);
        setPaywall(false);
        setToast('전체 게시물이 열렸어요');
      } else if (msg) setToast(msg);
    });

  const restore = async () => {
    const ok = await restorePurchase();
    if (ok) {
      setUnlocked(true);
      setPaywall(false);
      setToast('구매 내역을 복원했어요');
    } else setToast('복원할 구매 내역이 없어요');
  };

  const share = async () => {
    const message = '헤어질까, 버틸까. 흔들리는 연애를 해독해주는 이야기\n토스에서 "연애 해독" 검색해봐 👀';
    try {
      await Share.sendMessage({ message });
    } catch {
      try {
        await navigator.clipboard.writeText(message);
        setToast('문구를 복사했어요');
      } catch {
        setToast('공유를 지원하지 않는 환경이에요');
      }
    }
  };

  return (
    <main className="page home">
      <div className="hero">
        <img src="./art/detail_a1.jpg" alt="비 오는 밤, 열린 문 앞에 앉아 휴대폰을 보는 사람" />
        <div className="hero-fade" />
      </div>
      <p className="kicker">연애 해독 · @lovedecode101</p>
      <h1>
        헤어질까,
        <br />
        <em>버틸까.</em>
      </h1>
      <p className="lead">
        오래 만나서, 정 때문에, 혼자가 무서워서.
        <br />
        흔들리는 연애를 해독해주는 이야기를 모았어요.
      </p>

      <button className="guide-card" onClick={() => withAd(() => setGuide(true))}>
        <span className="tag">무료 읽을거리</span>
        <b>헤어질까 고민될 때 먼저 볼 6가지</b>
        <span className="guide-sub">존중 · 신뢰 · 마음의 온도 · 주고받기 · 싸움 뒤 회복 · 미래</span>
        <span className="arrow">읽기 ›</span>
      </button>

      <button className="guide-card alt" onClick={() => setCheck(true)}>
        <span className="tag">{QUESTIONS.length}문항 체크리스트</span>
        <b>우리 관계 자기 점검</b>
        <span className="guide-sub">최근 3개월을 떠올리며 체크하면 영역별 상태와 개선법을 알려드려요 · 결과 전 짧은 광고</span>
        <span className="arrow">시작 ›</span>
      </button>

      <section className="library">
        <div className="lib-head">
          <h3>연애 해독 게시물</h3>
          <span className="lib-sub">{unlocked ? '전편 열람 중' : `${FREE_COUNT}편 무료 · 열 때 가끔 짧은 광고`}</span>
        </div>
        <div className="grid">
          {POSTS.map((p, i) => {
            const locked = i >= FREE_COUNT && !unlocked;
            return (
              <button key={p.ep} className={`post ${locked ? 'locked' : ''}`} onClick={() => openPost(p.ep, i)}>
                <img src={slideSrc(p.ep, 1)} alt={p.title} loading="lazy" />
                {locked && (
                  <span className="lock">
                    <LockIcon />
                  </span>
                )}
                {i < FREE_COUNT && !unlocked && <span className="free">무료</span>}
              </button>
            );
          })}
        </div>
        {!unlocked && (
          <button className="unlock" onClick={() => setPaywall(true)}>
            <LockIcon /> 전체 게시물 평생 소장하기
          </button>
        )}
      </section>

      <button className="ghost wide" onClick={share}>
        친구에게 공유하기
      </button>
      <p className="disclaimer">
        연애 심리 콘텐츠예요. 전문 상담을 대신하지 않아요. 관계에서 위협이나 폭력을 느낀다면 112, 상담은 1366(24시간)이에요.
      </p>

      {guide && (
        <div className="reader">
          <div className="vtop">
            <span className="vtitle">헤어질까 고민될 때 먼저 볼 6가지</span>
            <button className="vclose" onClick={closeOverlay} aria-label="닫기">
              ✕
            </button>
          </div>
          <div className="reader-body">
            <p className="reader-lead">
              헤어짐을 고민하는 사람의 절반쯤은 떠날 이유와 머물 이유를 동시에 갖고 있어요. 흔들리는 게 정상이에요. 감정 말고
              아래 여섯 가지를 차분히 떠올려 보세요. 어디가 무너졌는지 보이면, 고칠지 정리할지도 보여요.
            </p>
            {SIGNS.map((s, n) => (
              <article className="card advice" key={s.key}>
                <span className="tag">
                  {String(n + 1).padStart(2, '0')} · {SIGN_LABEL[s.key]}
                </span>
                <h3>{s.title}</h3>
                <p className="why">{s.why}</p>
                <ul className="todo">
                  {s.todo.map((t) => (
                    <li key={t}>{t}</li>
                  ))}
                </ul>
              </article>
            ))}
            <article className="card">
              <span className="tag">마지막으로</span>
              <h3>사랑일까, 정일까</h3>
              <p className="why">
                오래 만날수록 "아까워서" 못 헤어지는 건 자연스러운 심리예요. 이미 쓴 시간은 돌아오지 않지만, 앞으로의 시간은 아직
                내 거예요. 이 사람이라서 머물고 싶은 마음이 남아 있다면 지금이 고칠 때고, 함께한 시간과 두려움만 남았다면 정리를
                준비할 때일 수 있어요.
              </p>
            </article>
            <article className="card safe">
              <span className="tag">꼭 기억하기</span>
              <h3>이건 고민할 문제가 아니에요</h3>
              <p className="why">
                휴대폰 감시, 친구 못 만나게 하기, "헤어지면 죽겠다"는 협박, 물건 던지기나 밀치기. 이런 행동은 연애의 문제가 아니라
                통제예요. 위급하면 112(문자 신고 가능), 상담은 1366(24시간)에서 도움받을 수 있어요.
              </p>
            </article>
            <p className="disclaimer">자가 점검을 돕는 글이에요. 관계의 결정은 언제나 당신의 몫이에요.</p>
          </div>
        </div>
      )}

      {check && <Checklist onClose={closeOverlay} />}

      {viewer && <Viewer ep={viewer} onClose={closeOverlay} />}

      {adGate && (
        <div className="sheet-bg" onClick={closeOverlay}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <h3>짧은 광고 후에 열려요</h3>
            <p>
              무료 글은 광고로 운영돼요.
              <br />
              광고가 끝나면 바로 글이 열려요.
            </p>
            <button className="cta" onClick={watchAdThenOpen}>
              광고 보고 글 보기
            </button>
            <button className="text-btn" onClick={() => { closeOverlay(); setPaywall(true); }}>
              광고 없이 전체 보기 (평생 소장)
            </button>
          </div>
        </div>
      )}

      {paywall && (
        <div className="sheet-bg" onClick={closeOverlay}>
          <div className="sheet" onClick={(e) => e.stopPropagation()}>
            <img className="sheet-art" src="./art/detail_a2.jpg" alt="" />
            <h3>연애 해독 전체 게시물</h3>
            <p>
              회피형·불안형·나르시시즘·가스라이팅까지
              <br />
              연재 게시물 전체를 한 번 결제로 평생 볼 수 있어요.
            </p>
            <ul className="sheet-list">
              <li>지금 공개된 {POSTS.length}편 전체 ({POSTS.length * SLIDES_PER_POST}장)</li>
              <li>매주 새 글 추가, 추가분도 계속 열람</li>
              <li>광고 없이 보기</li>
            </ul>
            <button className="cta" onClick={buy}>
              평생 소장하기
            </button>
            <button className="text-btn" onClick={restore}>
              이미 구매했어요 (구매 복원)
            </button>
          </div>
        </div>
      )}
      {toast && <div className="toast">{toast}</div>}
    </main>
  );
}

function Viewer({ ep, onClose }: { ep: string; onClose: () => void }) {
  const [cur, setCur] = useState(1);
  const ref = useRef<HTMLDivElement>(null);
  const post = useMemo(() => POSTS.find((p) => p.ep === ep), [ep]);
  const onScroll = () => {
    const el = ref.current;
    if (!el) return;
    setCur(Math.round(el.scrollLeft / el.clientWidth) + 1);
  };
  return (
    <div className="viewer">
      <div className="vtop">
        <span className="vtitle">{post?.title}</span>
        <button className="vclose" onClick={onClose} aria-label="닫기">
          ✕
        </button>
      </div>
      <div className="track" ref={ref} onScroll={onScroll}>
        {Array.from({ length: SLIDES_PER_POST }, (_, i) => (
          <img key={i} src={slideSrc(ep, i + 1)} alt={`${post?.title} ${i + 1}번째 장`} />
        ))}
      </div>
      <div className="vcount">
        {cur} / {SLIDES_PER_POST} · 옆으로 넘겨보세요
      </div>
    </div>
  );
}

function LockIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
      <rect x="5" y="10" width="14" height="10" rx="2" fill="currentColor" />
      <path d="M8 10V7a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" strokeWidth="2" />
    </svg>
  );
}

function Checklist({ onClose }: { onClose: () => void }) {
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [done, setDone] = useState(false);
  const [loading, setLoading] = useState(false);
  const body = useRef<HTMLDivElement>(null);

  useEffect(() => {
    body.current?.scrollTo(0, 0);
  }, [done, idx]);

  const pick = (v: number) => {
    const q = QUESTIONS[idx];
    const next = { ...answers, [q.id]: v };
    setAnswers(next);
    if (idx + 1 < QUESTIONS.length) {
      setTimeout(() => setIdx(idx + 1), 120);
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      if (adReady()) setReady(true);
      else setDone(true);
    }, 1200);
  };

  const [ready, setReady] = useState(false);
  const seeResult = () =>
    showAdThen(() => {
      setReady(false);
      setDone(true);
      preloadAd();
    });

  const restart = () => {
    setAnswers({});
    setIdx(0);
    setDone(false);
  };

  const s = computeScores(answers);
  const weak = weakest(s);
  const unsafe = ['s1', 's2', 's3', 's4'].some((id) => (answers[id] ?? 0) >= 1);

  return (
    <div className="reader">
      <div className="vtop">
        <span className="vtitle">우리 관계 자기 점검</span>
        <button className="vclose" onClick={onClose} aria-label="닫기">
          ✕
        </button>
      </div>
      <div className="reader-body" ref={body}>
        {ready ? (
          <div className="loading inline ready">
            <h3>점검이 끝났어요</h3>
            <p>
              결과를 보기 전에 <b>짧은 광고</b>가 재생돼요.
              <br />
              광고가 끝나면 바로 결과를 보여드릴게요.
            </p>
            <button className="cta" onClick={seeResult}>
              광고 보고 결과 확인하기
            </button>
          </div>
        ) : loading ? (
          <div className="loading inline">
            <p>체크한 내용을 정리하고 있어요</p>
          </div>
        ) : !done ? (
          <>
            <div className="qtop">
              <button className="back" disabled={idx === 0} onClick={() => setIdx(Math.max(0, idx - 1))} aria-label="이전 질문">
                ‹
              </button>
              <div className="progress">
                <div className="bar" style={{ width: `${((idx + 1) / QUESTIONS.length) * 100}%` }} />
              </div>
              <span className="count">
                {idx + 1}/{QUESTIONS.length}
              </span>
            </div>
            <p className="area">{DOMAIN_LABEL[QUESTIONS[idx].d]}</p>
            <h2 key={QUESTIONS[idx].id} className="question">
              {QUESTIONS[idx].q}
            </h2>
            <div className="scale" key={`s${QUESTIONS[idx].id}`}>
              {SCALE.map((label, v) => (
                <button key={v} className={`opt ${answers[QUESTIONS[idx].id] === v ? 'on' : ''}`} onClick={() => pick(v)}>
                  <span className={`dot d${v}`} />
                  {label}
                </button>
              ))}
            </div>
          </>
        ) : (
          <>
            {unsafe && (
              <article className="card safe">
                <span className="tag">먼저 꼭 확인해 주세요</span>
                <h3>체크한 항목 중에 안전과 관련된 것이 있어요</h3>
                <p className="why">
                  감시, 고립, 협박, 폭력은 대화로 고칠 연애 문제가 아니라 통제예요. 혼자 감당하지 마세요. 위급하면 112(문자 신고 가능),
                  상담은 1366(24시간)에서 도움받을 수 있어요.
                </p>
              </article>
            )}
            <article className="card">
              <h3>영역별 점검 결과</h3>
              <p className="card-sub">체크한 내용을 영역별로 모은 거예요. 높을수록 그 영역이 안정적이에요.</p>
              {HEALTH_DOMAINS.map((d) => {
                const h = health(s[d]);
                const tone = h >= 67 ? 'good' : h >= 40 ? 'mid' : 'bad';
                return (
                  <div className="meter" key={d}>
                    <span className="mlabel">{DOMAIN_LABEL[d]}</span>
                    <div className="mtrack">
                      <div className={`mfill ${tone}`} style={{ width: `${Math.max(h, 4)}%` }} />
                    </div>
                    <span className="mval">{h}</span>
                  </div>
                );
              })}
            </article>
            {weak.length === 0 ? (
              <article className="card">
                <h3>눈에 띄게 흔들리는 영역은 없어요</h3>
                <p className="why">
                  체크한 내용만 보면 여섯 영역이 대체로 안정적이에요. 그래도 마음이 불안하다면 '헤어질까 고민될 때 먼저 볼 6가지'를
                  함께 읽어보세요.
                </p>
              </article>
            ) : (
              <p className="reader-lead">상대적으로 낮게 나온 영역부터 살펴보세요.</p>
            )}
            {weak.map((d) => (
              <article className="card advice" key={d}>
                <span className="tag">{DOMAIN_LABEL[d]}</span>
                <h3>{ADVICE[d].title}</h3>
                <p className="why">{ADVICE[d].why}</p>
                <ul className="todo">
                  {ADVICE[d].todo.map((t) => (
                    <li key={t}>{t}</li>
                  ))}
                </ul>
              </article>
            ))}
            <p className="disclaimer">
              스스로 돌아보기 위한 체크리스트예요. 관계를 진단하거나 판정하지 않으며, 결정은 언제나 당신의 몫이에요.
            </p>
            <button className="ghost wide" onClick={restart}>
              다시 체크하기
            </button>
          </>
        )}
      </div>
    </div>
  );
}
