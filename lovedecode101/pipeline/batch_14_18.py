# 14~18호 원고 → body_NN.html, caption_NN.txt 생성
import os
here = os.path.dirname(os.path.abspath(__file__))
_B9 = open(f'{here}/body_09.html').read()
BG = {k: _B9[_B9.index(f'<div class="bg {k}"'):_B9.index('<div class="grain"', _B9.index(f'<div class="bg {k}"'))] for k in ['sil', 'hands']}


def bg(k):
    return BG[k] if k in BG else f'<div class="bg {k}"></div>'


def li(items):
    out = []
    for it in items:
        n, t = it[0], it[1]
        small = f'<small>{it[2]}</small>' if len(it) > 2 else ''
        body = f'<b>{t}</b>{small}' if small else t
        out.append(f'      <li data-n="{n}">{body}</li>')
    return '    <ul>\n' + '\n'.join(out) + '\n    </ul>'


def slide(i, k, chip, inner):
    return f'''
<!-- {i} -->
<section class="slide" id="s{i}">
  {bg(k)}<div class="grain"></div><div class="vig"></div>
  <span class="chip">{chip}</span><span class="num">{i} / 10</span>
  <div class="body">
{inner}
  </div>
  <span class="brand">@lovedecode101</span><div class="bar" style="width:calc(820px * {i*10} / 100)"></div>
</section>
'''


def P(t, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'    <p{c}>{t}</p>'


def H1(t):
    return f'    <h1>{t}</h1>'


def H2(t):
    return f'    <h2>{t}</h2>'


def EN(t):
    assert len(t) <= 220, (len(t), t)
    return f'    <p class="en">{t}</p>'


def STEPS(rows):
    s = '\n'.join(f'      <div class="step"><b>{a}</b><span>{b}</span></div>' for a, b in rows)
    return f'    <div class="steps">\n{s}\n    </div>'


def CTA(save, nxt):
    return f'    <div class="cta"><span>{save}</span><span>다음 편: {nxt}</span></div>'


EPS = {}

# ---------------- 14호 ----------------
EPS['14'] = dict(title='외향형 vs 불안형 구분법', next='회피형이 안정형으로 가는 길', slides=[
    slide(1, 'sil', '구분법', '\n'.join([
        H1('외향형<br>vs<br><em>불안형</em><br>구분법'),
        P('말이 빠르고 표현이 크다고<br>다 불안한 건 아닙니다', 'sub'),
        EN('Extrovert or anxiously attached? How to tell them apart. Talking fast and expressing big feelings does not automatically mean anxiety.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('적극적인 사람,<br>설렘일까 <em>경고</em>일까'),
        P('좋은 사람 같은데<br>속도가 너무 빨라요.<br>벌써 매일 통화하재요.<br>혹시 불안형일까요?', 'quote'),
        P('속도와 불안은 다른 문제입니다. 둘을 섞어 보면 좋은 사람을 놓칩니다.', 'sub'),
        EN('"They seem kind, but it\'s moving so fast. Daily calls already. Are they anxiously attached?" Speed and anxiety are different things. Mix them up and you may lose a good person.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('외향형은 원래<br><em>반응</em>을 먹고 삽니다'),
        P('외향형의 뇌는 웃음, 칭찬, 눈 맞춤에 보상 반응이 더 크게 일어나는 편입니다. 마음에 드는 사람 앞에선 빨리, 크게 표현합니다.'),
        P('인정받고 싶은 외향형은 이상한 게 아니라 기본값입니다.', 'sub'),
        EN('Extroverts run on reactions. Laughter, praise and eye contact light up their reward system, so they express interest fast and loud. Wanting recognition is their default, not a flaw.')])),
    slide(4, 'spot', '핵심', '\n'.join([
        H2('크기가 아니라<br><em>파도</em>를 보세요'),
        P('외향형이냐는 표현의 볼륨 문제. 불안형이냐는 감정이 얼마나 출렁이느냐의 문제. 재는 축이 다릅니다.'),
        STEPS([('볼륨', '말수, 속도, 표현의 크기 → 성향'), ('파도', '하루에도 오르내리는 기복 → 애착')]),
        EN('Watch the waves, not the volume. Extroversion is about how loud and fast someone expresses. Anxious attachment is about how much their mood swings. Two different scales.')])),
    slide(5, 'glass', '외향 불안형', '\n'.join([
        H2('어제는 폭죽,<br>오늘은 <em>서운함</em>'),
        li([('·', '애정 표현이 쏟아지다 갑자기 식음'), ('·', '답장 하나에 기분이 급변'), ('·', '서운함을 크게, 바로 터뜨림'), ('·', '"나 좋아해?" 확인이 반복됨')]),
        P('속의 불안이 걸러지지 않고 그대로 새어 나옵니다. 곁에 있는 사람은 날씨를 읽느라 지칩니다.', 'sub'),
        EN('The anxious extrovert: fireworks yesterday, hurt today. Affection floods then cools, one text flips the mood, hurt bursts out loudly, "Do you like me?" again and again. Partners get tired of reading the weather.')])),
    slide(6, 'lines', '외향 안정형', '\n'.join([
        H2('크게 말하지만<br><em>한결같다</em>'),
        li([('·', '표현은 많아도 대부분 웃음과 유머'), ('·', '짜증과 불안이 잘 새지 않음'), ('·', '지적도 "어떻게 하면 나을까"로'), ('·', '내 속도를 말하면 맞춰줌')]),
        P('목소리는 커도 하늘은 맑은 사람입니다.', 'sub'),
        EN('The secure extrovert: loud but steady. Mostly laughter and humor, little irritation leaking out, criticism framed as "how can this get better?", and they adjust when you ask for your pace.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('감정이 진한 사람도<br><em>불안형</em>은 아닙니다'),
        P('공감이 깊은 사람은 남의 마음을 금방 알아채는 만큼, 내 마음도 알아봐 주길 바랍니다. 초반엔 무겁게 느껴질 수 있습니다.'),
        li([('✕', '서운함을 매번 확인받아야 풀림 → 불안형'), ('○', '느낀 만큼 상대 마음도 살핌 → 안정형')]),
        EN('The twist: strong feelers aren\'t automatically anxious. They read emotions fast and hope to be cared for too. If they demand endless reassurance, that\'s anxiety. If they give care as richly as they feel, that\'s secure.')])),
    slide(8, 'glass', '만난다면', '\n'.join([
        H2('표현이 큰 사람 앞에서<br>지킬 <em>세 가지</em>'),
        STEPS([('속도', '"천천히 가자"는 거절이 아닙니다'), ('관찰', '첫 주의 과함보다 한 달 뒤의 편안함'), ('고요', '당신의 차분함은 이 관계의 닻입니다')]),
        P('맞춰주기만 하면 금방 지칩니다. 내 리듬도 관계의 재료입니다.'),
        EN('Three things to keep with an intense partner: asking to slow down is not rejection; judge by how calm it feels after a month, not the first week; your quiet is this relationship\'s anchor.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('이렇게 하면<br>좋은 사람도 <em>놓칩니다</em>'),
        li([('✕', '표현이 크다고 바로 불안형 판정', '볼륨은 성향, 기복이 애착입니다'), ('✕', '감정 표현을 "오버"라고 넘기기', '표현이 큰 사람은 무시에 더 크게 다칩니다'), ('✕', '부담을 참다가 말없이 멀어지기', '속도 얘기는 일찍 꺼낼수록 쉽습니다')]),
        EN('How to lose a good person: labeling them anxious just for being expressive, brushing off their feelings as "too much," or swallowing discomfort and quietly fading away. Talk about pace early.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '빠른 표현이 → 일관 vs 기복'), ('2', '함께 있으면 → 채워짐 vs 닳음'), ('3', '시간이 갈수록 → 안심 vs 불안')]),
        '    <div class="rule"></div>',
        P('볼륨은 성향,<br>파도는 애착.', 'big'),
        P('그 사람은 볼륨형인가요, 파도형인가요? 댓글로 알려주세요.', 'sub'),
        CTA('저장 → 두 번째 만남 전에 다시 보기', '회피형이 안정형으로 가는 길'),
        EN('Check: is their fast expression consistent or swinging? Do you feel filled or worn down together? Calmer or more anxious over time? Volume is personality. Waves are attachment.')])),
], caption='''표현이 크고 속도가 빠른 사람, 불안형 애착일까요 아니면 그냥 외향형일까요?

외향형인지는 표현의 볼륨으로, 불안형인지는 감정의 기복으로 봐야 합니다.
목소리가 커도 한결같은 사람이 있고, 조용해도 하루에 몇 번씩 출렁이는 사람이 있습니다.
"조금 천천히 가고 싶어"라는 말은 거절이 아니라 내 리듬을 지키는 말입니다.
단, 어떤 성향이든 상대를 판정하는 데 쓰기보다 한 달쯤 지켜보는 데 쓰세요.
다음 편은 "회피형이 안정형으로 가는 길"입니다.
지금 만나는 사람이 어느 쪽 같은지 댓글이나 DM으로 남겨주세요.

Fast and expressive doesn't mean anxiously attached. Extroversion is about volume; anxious attachment is about mood swings. Watch for consistency over a month, and feel free to ask for a slower pace.

관계를 이해하고 나를 지키기 위한 글입니다.

#불안형 #외향형 #애착유형 #연애심리 #MBTI''')

# ---------------- 15호 ----------------
EPS['15'] = dict(title='회피형이 안정형으로 가는 길', next='불안형이 안정형으로 가는 길', slides=[
    slide(1, 'sil', '회피형 편', '\n'.join([
        H1('회피형,<br><em>안정형</em><br>으로<br>가는 길'),
        P('혼자가 편한 사람이<br>함께도 편해지는 순서', 'sub'),
        EN('The path from avoidant to secure. A step-by-step order for someone who is comfortable alone to become comfortable together.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('가까워질수록<br><em>숨이 막혀요</em>'),
        P('좋아하는 사람인데<br>"보고 싶어" 한 마디에<br>갑자기 도망치고 싶어요.<br>저 고장 난 걸까요?', 'quote'),
        P('고장이 아니라 오래 써온 생존 방식입니다. 바꿀 수 있습니다.', 'sub'),
        EN('"I like them, but one \'I miss you\' makes me want to run. Am I broken?" Not broken. It\'s a survival habit you\'ve used for years, and it can change.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('그 거리두기는<br>한때 <em>나를 살렸습니다</em>'),
        P('기대면 실망하던 시절, 혼자 해결하는 건 가장 영리한 선택이었습니다. 문제는 지금도 모든 사람에게 같은 방식을 쓴다는 것.'),
        P('전략은 그대로인데, 상황이 바뀌었습니다.', 'sub'),
        EN('That distance once saved you. When leaning on people meant disappointment, handling everything alone was smart. The problem is using the same strategy on everyone now. The situation changed; the strategy didn\'t.')])),
    slide(4, 'spot', '대가', '\n'.join([
        H2('혼자가 편한 대신<br><em>잃는 것</em>들'),
        li([('·', '감정을 끄다 보니 기쁨도 같이 꺼짐'), ('·', '갈등을 피해 문제는 그대로 쌓임'), ('·', '가까운 사람일수록 단점만 보임'), ('·', '깊어질 때마다 출구부터 찾음')]),
        P('평온해 보이지만, 음소거된 평온입니다.', 'sub'),
        EN('What being comfortable alone costs: muting feelings mutes joy too, avoided conflicts pile up, the closer someone gets the more flaws you see, and depth makes you look for the exit. It\'s calm on mute.')])),
    slide(5, 'glass', '1단계', '\n'.join([
        H2('감정에<br><em>이름표</em>부터'),
        P('회피형은 감정을 못 느끼는 게 아니라, 느끼기 전에 꺼버립니다. 첫걸음은 끄기 전에 이름 붙이기.'),
        li([('○', '"지금 좀 답답해"'), ('○', '"이 말 듣고 살짝 겁났어"'), ('○', '하루 한 줄, 감정 단어 메모')]),
        EN('Step 1: label it before you switch it off. Avoidant people do feel, they just shut it down first. Try "I feel a bit stuck right now," "That scared me a little," and one feeling word in a note each day.')])),
    slide(6, 'lines', '2단계', '\n'.join([
        H2('사라지기 전에<br><em>예고</em>하기'),
        P('혼자만의 시간은 필요합니다. 문제는 말없이 사라지는 것. 상대에겐 그게 이별의 예고편처럼 보입니다.'),
        li([('✕', '읽고 답 없이 이틀 잠수'), ('○', '"오늘은 혼자 쉴게. 내일 연락할게"')]),
        EN('Step 2: announce before you disappear. Alone time is fine. Vanishing silently isn\'t; to a partner it looks like a breakup trailer. Not two days on read, but "I need a quiet night. I\'ll text you tomorrow."')])),
    slide(7, 'hands', '가장 실용적인 것', '\n'.join([
        H2('도망치고 싶을 때<br><em>10분</em>만 머물기'),
        P('친밀함이 커지는 순간, 몸이 먼저 출구를 찾습니다. 그때 자리를 뜨지 말고 딱 10분만 그대로 있어 보세요.'),
        P('10분 뒤에도 괜찮았다는 경험이 쌓이면, 뇌는 가까움을 위험 목록에서 하나씩 지웁니다.', 'sub'),
        EN('The most practical move: when closeness spikes and your body wants out, stay just ten more minutes. Each time it turns out fine, your brain removes closeness from its danger list a little more.')])),
    slide(8, 'glass', '3단계', '\n'.join([
        H2('완벽한 사람 말고<br><em>좋은 사람</em>을'),
        P('단점이 유독 크게 보인다면, 가까워지지 않으려는 핑계일 때가 많습니다.'),
        STEPS([('평가', '"이래서 안 돼"를 찾는 눈'), ('호기심', '"왜 그랬을까"를 묻는 눈')]),
        EN('Step 3: look for a good person, not a perfect one. When flaws suddenly look huge, it\'s often an excuse to stay distant. Swap the judging eye ("this is why it won\'t work") for a curious one ("why did they do that?").')])),
    slide(9, 'spot', '함정', '\n'.join([
        H2('이렇게 하면<br><em>제자리</em>입니다'),
        li([('✕', '"나는 원래 혼자가 맞아"', '정체성이 아니라 습관입니다'), ('✕', '한 번에 확 바뀌려 하기', '반동으로 더 멀리 튕겨 나갑니다'), ('✕', '상대에게 기다려달라고만 하기', '움직이는 쪽도 나여야 합니다')]),
        EN('Traps that keep you stuck: "I\'m just meant to be alone" (it\'s a habit, not identity), trying to change overnight (you bounce back further), only asking them to wait (you have to move too).')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '불편한 감정 → 이름 붙임 vs 끔'), ('2', '혼자이고 싶을 때 → 예고 vs 잠수'), ('3', '가까워지면 → 머문다 vs 출구')]),
        '    <div class="rule"></div>',
        P('혼자서도 괜찮은 사람이<br>함께여도 괜찮아질 때.', 'big'),
        P('가장 어려운 단계는 몇 번인가요? 댓글로 번호만 남겨주세요.', 'sub'),
        CTA('저장 → 도망치고 싶은 날 다시 보기', '불안형이 안정형으로 가는 길'),
        EN('Check: do you name uncomfortable feelings or switch them off? Announce alone time or vanish? Stay when it gets close or find the exit? Secure is when fine alone becomes fine together.')])),
], caption='''가까워질수록 도망치고 싶어진다면, 회피형 애착에서 안정형으로 가는 길은 이 순서입니다.

그 거리두기는 한때 나를 지켜준 생존 방식이었습니다. 다만 지금은 상황이 바뀌었습니다.
감정에 이름표 붙이기, 사라지기 전에 예고하기, 완벽한 사람 말고 좋은 사람 보기.
가장 실용적인 건 도망치고 싶은 순간 딱 10분만 머무는 것입니다.
단, 한 번에 확 바뀌려 하면 반동이 옵니다. 하나씩, 천천히 가세요.
다음 편은 "불안형이 안정형으로 가는 길"입니다.
세 단계 중 가장 어려운 걸 댓글이나 DM으로 남겨주세요.

Avoidance once kept you safe, but the situation has changed. Name feelings before shutting them off, announce alone time instead of vanishing, and when closeness makes you want to run, stay ten more minutes.

관계를 이해하고 나를 지키기 위한 글입니다.

#회피형 #안정형 #애착유형 #연애심리 #연애고민''')

# ---------------- 16호 ----------------
EPS['16'] = dict(title='불안형이 안정형으로 가는 길', next='혼란형이 안정형으로 가는 길', slides=[
    slide(1, 'sil', '불안형 편', '\n'.join([
        H1('불안형,<br><em>안정형</em><br>으로<br>가는 길'),
        P('사랑을 확인하는 사람에서<br>사랑을 믿는 사람으로', 'sub'),
        EN('The path from anxious to secure. From someone who keeps checking for love to someone who can trust it.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('답장 하나에<br>하루가 <em>흔들려요</em>'),
        P('한 시간만 답이 없어도<br>머릿속에 이별 장면이<br>다 그려져요.<br>저 너무 피곤해요.', 'quote'),
        P('그 피로는 사랑이 커서가 아니라, 경보기가 예민해서입니다.', 'sub'),
        EN('"One hour without a reply and I\'ve already pictured the breakup. I\'m exhausted." That exhaustion isn\'t about how much you love. It\'s about how sensitive your alarm is.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('불안은 사랑의 크기가<br>아니라 <em>경보기</em>입니다'),
        P('언제 올지 모르는 다정함을 기다리던 경험이 뇌에 예민한 경보기를 달았습니다. 작은 변화에도 울립니다.'),
        P('경보기를 부술 필요는 없습니다. 감도만 낮추면 됩니다.', 'sub'),
        EN('Anxiety isn\'t the size of your love, it\'s an alarm. Waiting for affection that came unpredictably installed a sensitive one in your brain. Don\'t smash it. Turn the sensitivity down.')])),
    slide(4, 'spot', '패턴', '\n'.join([
        H2('이럴 때<br><em>경보</em>가 울립니다'),
        li([('·', '연락 간격이 평소보다 벌어질 때'), ('·', '상대 표정이 조금 굳었을 때'), ('·', '상대가 혼자 시간을 원할 때'), ('·', '칭찬이 평소보다 짧을 때')]),
        P('사건은 작은데, 해석은 늘 최악으로 달려갑니다.', 'sub'),
        EN('When the alarm goes off: replies come slower than usual, their face looks a little tense, they want time alone, a compliment is shorter than usual. Small events, worst-case interpretations.')])),
    slide(5, 'glass', '1단계', '\n'.join([
        H2('울릴 때마다<br><em>기록</em>하기'),
        P('불안이 올라오면 연락보다 기록이 먼저. 무슨 일이 있었고, 무슨 생각이 들었고, 몇 점짜리인지.'),
        STEPS([('사건', '답장이 두 시간째 없음'), ('생각', '"나한테 질렸나"'), ('점수', '10점 중 8점')]),
        EN('Step 1: log every alarm before you text. What happened ("no reply for two hours"), what you thought ("they\'re tired of me"), how strong it is (8 out of 10). Writing it down slows the spiral.')])),
    slide(6, 'lines', '2단계', '\n'.join([
        H2('확인 대신<br><em>내 하루</em>로 돌아오기'),
        P('불안형의 하루는 상대를 중심으로 돕니다. 상대가 조용하면 내 하루도 멈춥니다.'),
        li([('○', '연락과 상관없는 내 일정 하나'), ('○', '혼자 해도 즐거운 취미 하나'), ('○', '연인 말고 기댈 사람 한 명')]),
        EN('Step 2: come back to your own day instead of checking. Anxious days orbit the partner; when they go quiet, everything stops. Keep one plan unrelated to texting, one solo hobby, one person besides your partner.')])),
    slide(7, 'hands', '가장 실용적인 것', '\n'.join([
        H2('보내기 전<br><em>30분</em> 규칙'),
        P('서운한 메시지는 써도 됩니다. 다만 30분 뒤에 다시 읽고 보내세요. 대부분은 고쳐 쓰거나 지우게 됩니다.'),
        li([('✕', '"왜 연락 안 해? 나 이제 싫어?"'), ('○', '"오늘 바빴어? 저녁에 통화할래?"')]),
        EN('The most practical rule: write the hurt message, then wait 30 minutes and reread before sending. Most get rewritten or deleted. Not "Why aren\'t you texting? Over me?" but "Busy day? Call tonight?"')])),
    slide(8, 'glass', '3단계', '\n'.join([
        H2('요구 말고<br><em>요청</em>으로'),
        STEPS([('요구', '"매일 연락해. 안 하면 서운해"'), ('요청', '"자기 전 한 줄이면 안심될 것 같아"')]),
        P('원하는 걸 정확히 말하는 건 집착이 아니라 자기표현입니다.'),
        EN('Step 3: request, don\'t demand. "Text me every day or I\'ll be hurt" is a demand. "One line before bed would really settle me" is a request. Saying exactly what you need is self-expression, not clinginess.')])),
    slide(9, 'spot', '함정', '\n'.join([
        H2('이렇게 하면<br>불안이 <em>더 커집니다</em>'),
        li([('✕', '상대 접속 시간 확인하기', '확인할수록 경보는 예민해집니다'), ('✕', '불안을 숨기고 괜찮은 척', '참다 터지면 더 크게 흔들립니다'), ('✕', '시험하듯 먼저 거리 두기', '상대도 나도 지쳐 갑니다')]),
        EN('Traps that make anxiety louder: checking when they were last online (it sharpens the alarm), hiding it and acting fine (it bursts later), pulling away to test them (it wears you both out).')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '연락이 늦으면 → 기록 vs 추궁'), ('2', '하루의 중심 → 나 vs 상대'), ('3', '원하는 게 있을 때 → 요청 vs 요구')]),
        '    <div class="rule"></div>',
        P('불안이 사라지는 게 아니라<br>불안보다 내가 커지는 것.', 'big'),
        P('오늘 내 불안은 10점 중 몇 점? 댓글로 숫자만 남겨주세요.', 'sub'),
        CTA('저장 → 답장 기다리는 날 다시 보기', '혼란형이 안정형으로 가는 길'),
        EN('Check: when replies are late, do you log it or interrogate? Is your day centered on you or them? Do you request or demand? Secure isn\'t anxiety disappearing. It\'s you growing bigger than it.')])),
], caption='''답장 하나에 하루가 흔들린다면, 불안형 애착에서 안정형으로 가는 길은 경보기의 감도를 낮추는 데서 시작합니다.

불안은 사랑의 크기가 아니라 예민해진 경보기입니다.
울릴 때마다 기록하기, 확인 대신 내 하루로 돌아오기, 요구 말고 요청으로 말하기.
가장 실용적인 건 서운한 메시지를 30분 뒤에 다시 읽고 보내는 것입니다.
단, 불안을 숨기고 괜찮은 척하는 건 해결이 아닙니다. 정확하게 말하는 연습이 먼저입니다.
다음 편은 "혼란형이 안정형으로 가는 길"입니다.
오늘 내 불안이 몇 점인지 댓글이나 DM으로 남겨주세요.

Anxiety isn't the size of your love; it's an oversensitive alarm. Log it before you text, come back to your own day, turn demands into requests, and reread any hurt message after 30 minutes before sending.

관계를 이해하고 나를 지키기 위한 글입니다.

#불안형 #안정형 #애착유형 #연애심리 #연애고민''')

# ---------------- 17호 ----------------
EPS['17'] = dict(title='혼란형이 안정형으로 가는 길', next='연인을 안정형으로 만드는 대화법', slides=[
    slide(1, 'sil', '혼란형 편', '\n'.join([
        H1('혼란형,<br><em>안정형</em><br>으로<br>가는 길'),
        P('다가가고 싶은 마음과<br>도망치고 싶은 마음 사이에서', 'sub'),
        EN('The path from disorganized (fearful) to secure. For someone caught between wanting closeness and wanting to run.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('붙잡고 싶은데<br>먼저 <em>밀어내요</em>'),
        P('잘해주면 의심되고<br>멀어지면 매달려요.<br>제가 저를 모르겠어요.<br>이것도 바뀌나요?', 'quote'),
        P('바뀔 수 있습니다. 다만 속도보다 일관성이 먼저입니다.', 'sub'),
        EN('"When they\'re kind, I get suspicious. When they pull back, I cling. I don\'t understand myself. Can this change?" Yes. But for this pattern, consistency matters more than speed.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('액셀과 브레이크를<br><em>동시에</em> 밟는 중'),
        P('가까워지고 싶은 마음과 상처받을까 두려운 마음이 한꺼번에 켜져 있습니다. 그래서 행동이 하루에도 반대로 튑니다.'),
        P('나쁜 사람이 아니라, 두 신호가 엉킨 사람입니다.', 'sub'),
        EN('Pressing the gas and the brake at once. The wish for closeness and the fear of getting hurt are both switched on, so behavior flips in opposite directions within a day. Not a bad person, just crossed signals.')])),
    slide(4, 'spot', '패턴', '\n'.join([
        H2('이런 순간이<br><em>반복</em>된다면'),
        li([('·', '다정함을 받으면 오히려 불안해짐'), ('·', '다투면 현실감이 흐려지는 느낌'), ('·', '버려지기 전에 먼저 끝내고 싶음'), ('·', '화해 후 다시 의심이 올라옴')]),
        P('여러 개가 겹친다면 진단이 아니라 출발점으로 삼으세요.', 'sub'),
        EN('If these repeat: kindness makes you uneasy, fights make things feel unreal, you want to end it before being left, doubt returns right after making up. Treat it as a starting point, not a diagnosis.')])),
    slide(5, 'glass', '1단계', '\n'.join([
        H2('먼저 <em>몸</em>을<br>가라앉히기'),
        P('혼란형의 감정은 생각보다 몸에서 먼저 터집니다. 판단은 몸이 가라앉은 다음입니다.'),
        li([('1', '발바닥 감각에 10초 집중'), ('2', '숨을 길게 내쉬기 세 번'), ('3', '지금 보이는 것 다섯 개 말하기')]),
        EN('Step 1: settle the body first. For this pattern, emotions erupt in the body before thoughts. Feel your feet for ten seconds, take three long exhales, name five things you can see. Decide only after that.')])),
    slide(6, 'lines', '2단계', '\n'.join([
        H2('감정과 결정 사이<br><em>시간차</em> 두기'),
        P('혼란형의 결정은 감정이 꼭대기일 때 내려집니다. "끝내자"도, "다시 만나자"도.'),
        li([('○', '큰 결정은 하루 뒤에'), ('○', '"지금은 결정하지 않을게" 말하기'), ('○', '결정 전 믿는 사람 한 명에게 묻기')]),
        EN('Step 2: put time between feeling and deciding. Big decisions, "let\'s end it" or "let\'s get back together," get made at the emotional peak. Wait a day, say "I won\'t decide now," and ask one trusted person first.')])),
    slide(7, 'hands', '가장 실용적인 것', '\n'.join([
        H2('내 신호를<br><em>미리</em> 알려두기'),
        P('혼란형이 가장 지치는 순간은 상대가 나를 오해할 때입니다. 차분한 날에 내 사용 설명서를 건네세요.'),
        li([('○', '"갑자기 차가워지면 무서워서 그래"'), ('○', '"그땐 쫓지 말고 하루만 기다려줘"')]),
        EN('The most practical move: share your signals in advance. On a calm day, hand over your user manual: "If I suddenly go cold, it\'s because I\'m scared. Don\'t chase me, just give me a day."')])),
    slide(8, 'glass', '3단계', '\n'.join([
        H2('작은 약속으로<br><em>일관성</em> 쌓기'),
        P('필요한 건 큰 결심이 아니라 예측 가능한 하루입니다.'),
        STEPS([('아침', '같은 시간에 일어나 한 줄 쓰기'), ('연락', '정해둔 시간에 한 번은 꼭'), ('밤', '오늘 지킨 약속 하나 적기')]),
        EN('Step 3: build consistency with small promises. What helps isn\'t a grand resolution but a predictable day. Wake at the same time and write one line, check in at a set time, note one promise you kept.')])),
    slide(9, 'spot', '주의', '\n'.join([
        H2('혼자 버티지<br><em>않아도</em> 됩니다'),
        li([('✕', '감정이 폭발한 날 관계 끝내기', '내일의 나는 다르게 생각합니다'), ('✕', '다정한 사람을 시험하기', '시험은 신뢰를 깎아 먹습니다'), ('○', '공황이나 멍한 느낌이 잦다면', '전문가와 함께 가는 게 빠른 길입니다')]),
        EN('Careful: don\'t end things on the day emotions explode, don\'t test kind people. If panic or a numb, unreal feeling comes often, walking this path with a professional is the faster way.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '다정함을 받으면 → 안심 vs 의심'), ('2', '큰 결정은 → 하루 뒤 vs 그 자리'), ('3', '무서울 때 → 말한다 vs 밀어낸다')]),
        '    <div class="rule"></div>',
        P('흔들려도 괜찮습니다.<br>방향만 맞으면.', 'big'),
        P('오늘 지킬 작은 약속 하나, 댓글로 적어주세요.', 'sub'),
        CTA('저장 → 마음이 엉킨 날 다시 보기', '연인을 안정형으로 만드는 대화법'),
        EN('Check: does kindness bring relief or suspicion? Big decisions after a day or on the spot? When scared, do you say it or push away? Wobbling is okay, as long as you\'re heading the right way.')])),
], caption='''다가가고 싶은데 먼저 밀어낸다면, 혼란형 애착에서 안정형으로 가는 길은 속도보다 일관성입니다.

혼란형은 가까워지고 싶은 마음과 상처받을까 두려운 마음이 동시에 켜진 상태입니다.
먼저 몸을 가라앉히고, 감정과 결정 사이에 하루를 두고, 작은 약속으로 예측 가능한 하루를 쌓으세요.
가장 실용적인 건 차분한 날 연인에게 내 신호를 미리 알려두는 것입니다.
단, 공황이나 현실감이 흐려지는 느낌이 잦다면 혼자 버티지 말고 전문가의 도움을 받으세요.
다음 편은 "연인을 안정형으로 만드는 대화법"입니다.
오늘 지킬 작은 약속을 댓글이나 DM으로 남겨주세요.

Disorganized attachment is pressing the gas and brake at once. Settle the body first, put a day between feeling and deciding, build predictable days with small promises, and tell your partner your signals on a calm day.

관계를 이해하고 나를 지키기 위한 글입니다.

#혼란형 #안정형 #애착유형 #연애심리 #연애고민''')

# ---------------- 18호 ----------------
EPS['18'] = dict(title='연인을 안정형으로 만드는 대화법', next='퀀텀점프 원리: 관계가 한 번에 바뀌는 순간', slides=[
    slide(1, 'sil', '대화법', '\n'.join([
        H1('연인을<br><em>안정형</em>으로<br>만드는<br>대화법'),
        P('고치려는 순간 멀어지고<br>함께하자는 순간 가까워집니다', 'sub'),
        EN('How to talk so your partner can feel more secure. Trying to fix them pushes them away. Inviting them to grow together brings them closer.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('"너 회피형이잖아"<br>그 말 뒤로 <em>더 멀어졌어요</em>'),
        P('애착 글을 보여주며<br>같이 고쳐보자 했는데<br>오히려 말이 줄었어요.<br>뭘 잘못한 걸까요?', 'quote'),
        P('내용은 맞았을지 몰라도, 순서가 틀렸습니다.', 'sub'),
        EN('"I showed them an article on attachment and said let\'s fix it. Now they talk even less. What did I do wrong?" The content may have been right. The order was wrong.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('라벨을 붙이면<br>뇌는 <em>방패</em>를 듭니다'),
        P('"넌 OO형이야"를 듣는 순간 사람은 생각보다 방어를 먼저 합니다. 그리고 그 라벨대로 더 움직입니다.'),
        P('진단은 상담실의 일. 연인의 일은 곁에 있는 것입니다.', 'sub'),
        EN('Labels raise shields. Hearing "you\'re the avoidant type" puts people on defense before they think, and they often act even more like the label. Diagnosing is a therapist\'s job. A partner\'s job is to be there.')])),
    slide(4, 'spot', '첫 문장', '\n'.join([
        H2('상대 말고<br><em>나</em>로 시작하기'),
        li([('✕', '"너 불안정 애착이니까 고쳐"'), ('○', '"나도 불안할 때가 있어서 기록해보려고"'), ('○', '"같이 해볼래? 싫으면 나 혼자 할게"')]),
        P('먼저 걷는 사람을 보면 따라 걷고 싶어집니다.', 'sub'),
        EN('Start with "I," not "you." Not "You\'re insecure, fix it," but "I get anxious too, so I\'m going to track it. Want to try with me? If not, I\'ll do it alone." People want to walk beside someone already walking.')])),
    slide(5, 'glass', '대화 1', '\n'.join([
        H2('하루 10분,<br><em>마음 브리핑</em>'),
        P('해결하는 대화 말고 들여다보는 대화. 잠들기 전 10분이면 충분합니다.'),
        li([('1', '"오늘 제일 좋았던 순간은?"'), ('2', '"오늘 나한테 바랐던 게 있었어?"'), ('3', '"요즘 언제 제일 너다웠어?"')]),
        EN('Talk 1: a ten-minute heart briefing. Not a problem-solving talk, a looking-in talk. Before bed: "Best moment today?" "Anything you wished I\'d done today?" "When did you feel most like yourself lately?"')])),
    slide(6, 'lines', '대화 2', '\n'.join([
        H2('한 마디만<br><em>바꿔도</em>'),
        li([('✕', '"또 시작이네"', '→ "지금 많이 힘들구나"'), ('✕', '"그게 그렇게 서운해?"', '→ "어떤 부분이 제일 서운했어?"'), ('✕', '"넌 왜 맨날 그래"', '→ "요즘 뭐가 제일 버거워?"')]),
        EN('Talk 2: change one line. "Here we go again" → "This is really hard for you." "Is that really so upsetting?" → "Which part hurt most?" "Why are you always like this?" → "What\'s weighing on you most lately?"')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('불안을 고치지 말고<br><em>받아주기</em>'),
        P('불안한 사람에게 "그럴 필요 없어"는 문을 닫는 말입니다. 먼저 인정해주면 불안은 오히려 빨리 가라앉습니다.'),
        li([('○', '"그렇게 느낄 수 있지. 나 여기 있어"'), ('○', '"말해줘서 고마워"')]),
        EN('The twist: don\'t fix the anxiety, receive it. "There\'s no need to feel that way" shuts the door. Acknowledging it calms it faster: "It makes sense you feel that. I\'m here." "Thank you for telling me."')])),
    slide(8, 'glass', '말 없는 대화', '\n'.join([
        H2('말보다 오래 남는<br><em>세 가지</em>'),
        STEPS([('포옹', '만날 때, 헤어질 때 20초 천천히'), ('의식', '둘만 아는 인사, 둘만의 잘 자'), ('나란히', '말 없이 곁에 머무는 30분')]),
        P('예측 가능한 다정함이 쌓이면, 불안한 뇌는 조금씩 경계를 풉니다.'),
        EN('Three wordless conversations: a slow 20-second hug when meeting and parting, little rituals only you two share, and 30 quiet minutes simply staying side by side. Predictable warmth lowers guard.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('이건 대화가 아니라<br><em>판결</em>입니다'),
        li([('✕', '"너 그거 애착 문제야"', '진단은 대화의 문을 닫습니다'), ('✕', '한꺼번에 다 바꾸려 하기', '둘만 골라 한 달씩'), ('✕', '변화가 없다고 점수 매기기', '관계는 시험이 아니라 연습입니다')]),
        EN('These are verdicts, not conversation: "That\'s your attachment issue" (diagnosis closes the door), trying to change everything at once (pick two, one month each), scoring their progress (it\'s practice, not a test).')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '문제를 말할 때 → 나 vs 너'), ('2', '불안 앞에서 → 인정 vs 설득'), ('3', '변화는 → 함께 vs 강요')]),
        '    <div class="rule"></div>',
        P('사람은 고쳐지지 않습니다.<br>곁에서 자랄 뿐.', 'big'),
        P('연인에게 오늘 건네고 싶은 한 문장, 댓글로 남겨주세요.', 'sub'),
        CTA('저장 → 대화가 막힌 날 다시 보기', '퀀텀점프 원리: 관계가 한 번에 바뀌는 순간'),
        EN('Check: do you start with "I" or "you"? Do you acknowledge anxiety or argue with it? Is change shared or forced? People don\'t get fixed. They grow beside someone.')])),
], caption='''연인에게 "너 회피형이잖아", "불안형이니까 고쳐"라고 말해본 적 있나요? 애착유형은 라벨로 바뀌지 않습니다.

라벨을 붙이는 순간 사람은 방어부터 하고, 그 라벨대로 더 움직이게 됩니다.
그래서 첫 문장은 상대가 아니라 나로 시작해야 합니다. "나도 불안할 때가 있어서 해보려고."
하루 10분 마음 브리핑, 한 마디 바꾸기, 불안을 고치지 말고 받아주기.
단, 한꺼번에 다 하려 하지 말고 두 가지만 골라 한 달씩 해보세요.
다음 편은 "퀀텀점프 원리: 관계가 한 번에 바뀌는 순간"입니다.
연인에게 건네고 싶은 한 문장을 댓글이나 DM으로 남겨주세요.

Labels raise shields. Start with "I," not "you." Try a ten-minute nightly check-in, swap one harsh line for a curious one, and receive anxiety instead of arguing with it. People don't get fixed; they grow beside someone.

관계를 이해하고 나를 지키기 위한 글입니다.

#애착유형 #안정형 #불안형 #회피형 #연애심리''')

for n, ep in EPS.items():
    open(f'{here}/body_{n}.html', 'w').write(''.join(ep['slides']))
    open(f'{here}/caption_{n}.txt', 'w').write(ep['caption'].strip() + '\n')
    print(n, ep['title'])
import json
json.dump({n: {'title': e['title'], 'next': e['next']} for n, e in EPS.items()}, open(f'{here}/batch_14_18.json', 'w'), ensure_ascii=False)
