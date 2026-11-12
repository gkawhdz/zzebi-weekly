# 9~13호 원고 → body_NN.html, caption_NN.txt 생성
import os
here = os.path.dirname(os.path.abspath(__file__))
BG = {k: open(f'/tmp/bg_{k}.html').read() if os.path.exists(f'/tmp/bg_{k}.html') else f'<div class="bg {k}"></div>' for k in ['sil', 'hands', 'cat']}


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

# ---------------- 9호 ----------------
EPS['09'] = dict(title='우아한 안정형 되는 법', next='진지한 연애, 구식일까', slides=[
    slide(1, 'sil', '안정형 편', '\n'.join([
        H1('우아한<br>안정형<br><em>되는 법</em>'),
        P('타고나는 게 아닙니다.<br>먼저 입어보고, 몸에 맞춰가는 겁니다', 'sub'),
        EN('How to become gracefully secure. It is not something you are born with. You put it on first, and it slowly starts to fit.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('왜 그 사람 옆은<br><em>편안할까</em>'),
        P('잘생긴 것도 아닌데<br>다들 그 사람만 찾아요.<br>저는 노력해도 늘<br>애쓰는 사람 같고요.', 'quote'),
        P('차이는 얼굴이 아니라 태도입니다. 그리고 태도는 연습됩니다.', 'sub'),
        EN('"They\'re not even that good-looking, yet everyone gravitates to them. I try hard and still look like I\'m trying." The gap is not looks. It\'s posture. And posture can be practiced.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('애착은 못 바꿔도<br><em>행동</em>은 바꿉니다'),
        P('사람들은 마음이 바뀌어야 행동이 바뀐다고 믿습니다. 순서가 반대입니다.'),
        li([('1', '행동을 먼저 바꾸고'), ('2', '반복이 태도를 만들고'), ('3', '태도가 쌓여 정체성이 됩니다')]),
        P('웃어서 덜 긴장되는 날이 있잖아요. 뇌는 몸이 하는 걸 믿습니다.', 'sub'),
        EN('You can\'t rewire attachment by willpower, but you can change behavior. Act first, repeat until it becomes attitude, and attitude becomes identity. The brain believes what the body does.')])),
    slide(4, 'spot', '임시 장착', '\n'.join([
        H2('안정형인 척,<br>3주만 해보세요'),
        P('처음엔 어색합니다. "이건 내가 아닌데" 하는 저항이 올라옵니다. 정상입니다. 새 신발도 처음엔 뒤꿈치가 까집니다.'),
        P('같은 동작을 3주 반복하면 뇌는 그걸 원래 내 것으로 분류합니다. 연기가 습관이 되는 지점입니다.', 'sub'),
        EN('Wear "secure" like a borrowed jacket for three weeks. It will feel fake. That resistance is normal, like breaking in new shoes. After about 21 days of repetition, the brain files it as yours.')])),
    slide(5, 'glass', '행동 1 · 2', '\n'.join([
        H2('표정을 풀고,<br>말 대신 <em>귀</em>를'),
        li([('1', '만나기 전 거울 앞 3초, 입꼬리 올리기'), ('2', '상대 말 끝나고 3초 기다렸다 답하기'), ('3', '휴대폰은 가방 안으로'), ('4', '"그래서 어떻게 됐어?" 한 번 더 묻기')]),
        P('부드러운 얼굴과 끝까지 듣는 귀. 상대는 "내가 중요한 사람이구나"를 느낍니다.', 'sub'),
        EN('Behaviors 1 and 2: soften your face and lend your ears. Three seconds of a relaxed smile before meeting. Wait three seconds before replying. Phone away. Ask one follow-up question. People feel important near you.')])),
    slide(6, 'lines', '행동 3 · 4', '\n'.join([
        H2('자랑도 자책도 없이<br><em>있는 그대로</em>'),
        P('불안한 사람은 둘 중 하나로 흔들립니다. 과하게 부풀리거나, 일부러 깎아내리거나. 둘 다 "나 괜찮은 사람 맞지?"라는 질문입니다.'),
        li([('○', '칭찬엔 "고마워" 한 마디로 끝'), ('○', '실수엔 변명 없이 "다음엔 이렇게"'), ('○', '잘한 일은 담담하게 사실만')]),
        EN('Behaviors 3 and 4: no bragging, no self-shrinking. Both swings ask "Am I okay?" Answer praise with just "thanks." Own mistakes without excuses. State wins as plain facts. Presence grows from that calm.')])),
    slide(7, 'hands', '가장 실용적인 것', '\n'.join([
        H2('해석 하나만<br><em>바꿔보세요</em>'),
        P('답장이 늦을 때 불안형의 뇌는 "식었나"로 갑니다. 안정형의 뇌는 "바쁜가 보다"로 갑니다. 같은 사건, 다른 렌즈입니다.'),
        li([('✕', '"나한테 관심 없나 봐"'), ('○', '"바쁜 날인가 보다, 저녁에 물어보자"')]),
        P('오늘부터 불안한 해석이 떠오르면 두 번째 해석을 하나 더 붙이세요. 그게 긍정 렌즈 장착입니다.', 'sub'),
        EN('Behavior 5, the most practical: swap the lens. A late reply makes an anxious brain think "they\'re losing interest." A secure brain thinks "busy day, I\'ll ask tonight." Add a second reading every time.')])),
    slide(8, 'glass', '유형별', '\n'.join([
        H2('어디서 시작할지<br>유형마다 다릅니다'),
        STEPS([('불안형', '렌즈 바꾸기부터. 해석 하나가 하루를 살립니다'), ('회피형', '경청부터. 한 번 더 묻는 연습이 거리를 줄입니다'), ('안정형', '표정과 담담함. 이미 있는 걸 더 또렷하게')]),
        P('전부 하려 하지 마세요. 하나를 3주. 그게 순서입니다.'),
        EN('Where to start depends on you. Anxious: change the lens first. Avoidant: practice listening and one more question. Secure: sharpen the calm you already have. One habit for three weeks, then the next.')])),
    slide(9, 'spot', '함정', '\n'.join([
        H2('이렇게 하면<br><em>흉내</em>로 끝납니다'),
        li([('✕', '"나 원래 이런 사람 아닌데"', '정체성은 원래 고정된 게 아닙니다'), ('✕', '하루 해보고 효과 따지기', '뇌가 받아들이는 데 3주가 걸립니다'), ('✕', '상대 반응에 맞춰 껐다 켜기', '나를 위한 연습이지 연기가 아닙니다')]),
        EN('Traps that keep it fake: "This isn\'t who I am" (identity isn\'t fixed), judging after one day (the brain needs about three weeks), switching it on and off for someone\'s reaction (it\'s practice for you, not a show).')])),
    slide(10, 'cold', '오늘의 한 줄', '\n'.join([
        li([('1', '거울 앞 3초, 입꼬리'), ('2', '3초 기다리고 대답'), ('3', '불안한 해석에 두 번째 해석')]),
        '    <div class="rule"></div>',
        P('우아함은 타고난 게 아니라<br>반복한 행동의 다른 이름.', 'big'),
        P('어떤 행동부터 장착할지 댓글로 하나만 적어주세요. 3주 뒤에 다시 물어볼게요.', 'sub'),
        CTA('저장 → 3주 동안 매일 아침 보기', '진지한 연애, 구식일까'),
        EN('Today: three seconds of a soft smile, three seconds before replying, a second reading for every anxious thought. Grace isn\'t inborn. It\'s repeated behavior. Comment which one you\'ll start with.')])),
], caption='''안정형 애착인 사람 옆은 왜 이렇게 편안할까요?

차이는 외모가 아니라 태도이고, 태도는 연습으로 바뀝니다.
마음이 먼저 바뀌길 기다리지 말고, 행동을 3주만 먼저 입어보세요.
미소, 3초 경청, 담담한 말투, 그리고 불안한 해석에 두 번째 해석 붙이기.
하루 만에 바뀌는 건 없습니다. 하나씩, 3주씩입니다.
다음 편은 "진지한 연애, 구식일까"입니다.
어떤 행동부터 시작할지 댓글로 남겨주세요.

Why do some people feel so easy to be around? It's not looks, it's posture, and posture can be practiced. Don't wait to feel secure. Act secure for three weeks: a soft face, patient listening, calm words, and a second reading for every anxious thought.

관계를 이해하고 나를 지키기 위한 글입니다.

#안정형 #애착유형 #연애심리 #자존감 #연애고민''')

# ---------------- 10호 ----------------
EPS['10'] = dict(title='진지한 연애, 구식일까', next='방어기제 세련되게 바꾸는 법', slides=[
    slide(1, 'sil', '진지함 편', '\n'.join([
        H1('진지한<br>연애,<br><em>구식</em><br>일까'),
        P('가볍게 만나는 척하는 세상에서<br>진지함을 매력으로 쓰는 법', 'sub'),
        EN('Is wanting a serious relationship old-fashioned? How to turn seriousness into an asset in a world that pretends to date lightly.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('결혼까지 생각하는 게<br><em>촌스러운</em> 건가요'),
        P('요즘은 다 가볍게<br>만나는 것 같아요.<br>저만 너무 무겁게<br>구는 걸까요?', 'quote'),
        P('아니요. 다만 진지함에도 두 종류가 있습니다.', 'sub'),
        EN('"Is it uncool to think about marriage? Everyone seems to date casually. Am I too heavy?" No. But there are two kinds of seriousness, and only one of them pushes people away.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('다들 가벼운 척,<br>속으론 <em>오래</em> 원합니다'),
        P('설문에선 "쿨하게"가 유행어지만, 막상 고르라면 대부분 진지한 만남을 고릅니다. 겉과 속이 다른 시장입니다.'),
        P('가볍게 시작하는 이유는 하나. 헤어졌을 때 덜 아프려고 미리 깔아두는 안전장치입니다.', 'sub'),
        EN('Everyone acts casual, but most want something lasting. Surveys love "cool dating," yet people pick serious relationships when asked to choose. Going light is a safety net against the pain of a breakup.')])),
    slide(4, 'spot', '진짜 문제', '\n'.join([
        H2('사람들이 피하는 건<br>진지함이 아니라 <em>무게</em>'),
        li([('✕', '석 달 만에 "우리 결혼 언제 해?"'), ('✕', '"난 이렇게 진지한데 넌 왜 가벼워"'), ('✕', '작은 실수도 용납 안 되는 완벽함'), ('✕', '진지함을 핑계로 기대기')]),
        P('이건 진지함이 아니라 압박입니다. 상대는 미래가 아니라 시험을 느낍니다.', 'sub'),
        EN('What people avoid isn\'t seriousness, it\'s weight: "When are we getting married?" at month three, blaming them for being casual, zero tolerance for mistakes, leaning on them in the name of commitment.')])),
    slide(5, 'glass', '원칙 1', '\n'.join([
        H2('목표는 품되<br>속도는 <em>상대</em>에게'),
        P('결혼을 원한다는 사실은 숨길 필요 없습니다. 다만 일정표처럼 들이밀지 마세요.'),
        li([('○', '"나는 오래 가는 관계를 좋아해"'), ('✕', '"올해 안에 상견례 하자"')]),
        P('방향은 말하고, 속도는 함께 정하는 것. 그게 가벼워 보이지 않으면서 무겁지도 않은 진지함입니다.', 'sub'),
        EN('Hold the goal, share the pace. Don\'t hide that you want something lasting, just don\'t present it like a schedule. "I like relationships that last" works. "Let\'s meet the parents this year" doesn\'t.')])),
    slide(6, 'lines', '원칙 2', '\n'.join([
        H2('진지함을 말이 아니라<br><em>일관성</em>으로'),
        P('진지한 사람은 선언하지 않습니다. 약속 시간, 답장 리듬, 한 말을 지키는 태도로 보여줍니다.'),
        li([('1', '한 말은 작은 것까지 지키기'), ('2', '바빠도 연락 리듬은 일정하게'), ('3', '갈등 때도 같은 사람으로 남기')]),
        EN('Show seriousness through consistency, not declarations. Keep small promises, keep a steady texting rhythm even when busy, and stay the same person during conflict. People trust patterns, not speeches.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('진지한 사람일수록<br><em>가볍게</em> 웃어야 합니다'),
        P('무게 있는 마음엔 가벼운 표면이 필요합니다. 농담 한 줄, 여유 있는 표정이 "이 사람과 오래 있어도 숨 막히지 않겠다"는 신호가 됩니다.'),
        P('진지함은 뿌리에, 가벼움은 잎에. 둘 다 있어야 오래 갑니다.', 'sub'),
        EN('The twist: the more serious you are, the lighter you should smile. A heavy heart needs a light surface. A joke and an easy face signal "I won\'t feel suffocated with this person." Roots serious, leaves light.')])),
    slide(8, 'glass', '어디서 만날까', '\n'.join([
        H2('진지한 사람은<br>진지한 <em>장소</em>에'),
        STEPS([('취미 모임', '반복해서 만나며 일관성을 볼 수 있는 곳'), ('지인 소개', '검증된 신뢰가 깔린 출발점'), ('목적형 앱', '프로필에 원하는 관계를 적어두기')]),
        P('찾는 사람과 장소가 어긋나면 진지함은 "부담"으로만 읽힙니다.'),
        EN('Look for serious people where seriousness lives: hobby groups you attend repeatedly, introductions from friends, apps where you state the relationship you want. Wrong place, and seriousness reads as pressure.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('진지함이<br><em>독</em>이 되는 말'),
        li([('✕', '"나 진지한 거 알지? 그러니까…"', '진지함을 협상 카드로 쓰는 순간'), ('✕', '"우리 어차피 결혼할 거잖아"', '상대 선택지를 미리 지우는 말'), ('✕', '"가벼운 사람들 다 한심해"', '내 기준으로 남을 깎는 태도')]),
        EN('Lines that turn seriousness toxic: "You know I\'m serious, so..." (using it as leverage), "We\'re getting married anyway" (erasing their choice), "Casual people are pathetic" (judging others by your rule).')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '미래 얘기 → 방향 vs 일정표'), ('2', '진지함 → 행동 vs 선언'), ('3', '함께 있을 때 → 여유 vs 시험')]),
        '    <div class="rule"></div>',
        P('진지함은 구식이 아닙니다.<br>무거움이 구식입니다.', 'big'),
        P('당신의 진지함은 어느 쪽인가요? 댓글로 하나만 골라주세요.', 'sub'),
        CTA('저장 → 소개팅 전에 다시 보기', '방어기제 세련되게 바꾸는 법'),
        EN('Check: when you talk future, is it direction or a schedule? Is your seriousness shown or announced? Does time with you feel easy or like a test? Seriousness isn\'t outdated. Heaviness is.')])),
], caption='''진지한 연애를 원하면 촌스러운 걸까요? 애착유형과 상관없이 많은 분들이 묻는 질문입니다.

사람들이 피하는 건 진지함이 아니라 무게입니다.
목표는 품되 속도는 함께 정하고, 진지함은 선언 대신 일관성으로 보여주세요.
마음이 무거울수록 표면은 가볍게. 그래야 오래 갑니다.
단, 상대가 원하는 관계가 처음부터 다르다면 맞추려 애쓰기보다 확인이 먼저입니다.
다음 편은 "방어기제 세련되게 바꾸는 법"입니다.
비슷한 고민이 있다면 댓글이나 DM으로 남겨주세요.

Wanting a serious relationship isn't old-fashioned. What people avoid is heaviness: pressure, timelines, guilt. Hold the goal, share the pace, prove it with consistency, and keep a light surface over a serious heart.

관계를 이해하고 나를 지키기 위한 글입니다.

#연애심리 #애착유형 #진지한연애 #연애고민 #안정형''')

# ---------------- 11호 ----------------
EPS['11'] = dict(title='방어기제 세련되게 바꾸는 법', next='사랑받고 자란 사람 구분법', slides=[
    slide(1, 'sil', '방어기제 편', '\n'.join([
        H1('방어기제,<br><em>세련되게</em><br>바꾸는<br>법'),
        P('없애는 게 아니라<br>지금의 나에게 맞게 업데이트하는 것', 'sub'),
        EN('How to upgrade your defense mechanisms. Not deleting them, updating them to fit who you are now.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('좋은 사람인데<br>왜 <em>오래</em> 못 갈까요'),
        P('처음엔 다들 좋아해요.<br>그런데 몇 달 지나면<br>"너랑 있으면 피곤해"<br>라는 말을 들어요.', 'quote'),
        P('성격 문제가 아닐 수 있습니다. 오래된 보호막이 아직 켜져 있는 겁니다.', 'sub'),
        EN('"People like me at first, but months later they say I\'m exhausting." It may not be personality. It may be an old shield that never got switched off.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('방어기제는 나쁜 게 아니라<br><em>낡은</em> 겁니다'),
        P('어릴 때 상처받지 않으려고 뇌가 깔아둔 생존 프로그램. 그땐 나를 지켰습니다. 문제는 어른이 된 지금도 같은 버전으로 돌고 있다는 것.'),
        P('지울 필요 없습니다. 업데이트하면 됩니다.', 'sub'),
        EN('Defenses aren\'t bad, just outdated. They\'re survival programs your brain installed as a kid. Back then they protected you. The issue is running the same version as an adult. Don\'t delete it. Update it.')])),
    slide(4, 'spot', '유형 1 · 2', '\n'.join([
        H2('말이 넘치거나,<br>뭐든 <em>괜찮다</em>거나'),
        STEPS([('수다형', '침묵이 불안해 말로 덮는 과보상. "내 얘기 말고, 오늘 어땠어?"'), ('착한형', '거절이 버림받음 같아 다 맞추는 순응. 하루 하나 내 취향 말하기')]),
        P('침묵 3초는 위험이 아니라 신뢰입니다. 작은 취향 하나가 경계를 세웁니다.', 'sub'),
        EN('Types 1 and 2. The over-talker fills silence to hide anxiety: hand the turn back with "How was your day?" The people-pleaser agrees to everything: state one small preference a day. Three seconds of silence is trust.')])),
    slide(5, 'glass', '유형 3 · 4', '\n'.join([
        H2('쿨한 척하거나,<br><em>센</em> 척하거나'),
        STEPS([('쿨병형', '신경 쓰이는데 "괜찮아". 감정을 잘라내는 격리'), ('허세형', '약해 보일까 부풀리는 과시. 실은 인정받고 싶은 마음')]),
        li([('○', '"사실 좀 신경 쓰였어"'), ('○', '"이건 아직 잘 몰라. 알려줄래?"')]),
        EN('Types 3 and 4. The fake-cool says "it\'s fine" while hurting; the show-off inflates to avoid looking weak. Updated versions: "Honestly, that bothered me a bit." "I don\'t know this well yet, can you show me?"')])),
    slide(6, 'lines', '유형 5 · 6', '\n'.join([
        H2('해명부터 하거나,<br><em>남 탓</em>부터 하거나'),
        STEPS([('해명봇', '잘못을 인정하면 무너질 것 같아 이유부터 쌓는 합리화'), ('남탓형', '내 불편을 상대 문제로 돌리는 투사')]),
        P('둘 다 "내가 틀리면 끝"이라는 공포에서 나옵니다. 틀려도 끝나지 않는다는 경험이 해독제입니다.', 'sub'),
        EN('Types 5 and 6. The explainer stacks reasons instead of owning it; the blamer projects discomfort onto the partner. Both fear "if I\'m wrong, it\'s over." The antidote: learning that being wrong isn\'t the end.')])),
    slide(7, 'hands', '세 문장 공식', '\n'.join([
        H2('어떤 유형이든<br>이 <em>세 문장</em>이면 됩니다'),
        li([('1', '감정 이름 붙이기', '"지금 좀 긴장했어"'), ('2', '책임과 경계', '"방금 건 내 실수야 / 이건 불편해"'), ('3', '함께 다음 수', '"다음엔 이렇게 해볼게. 넌 어때?"')]),
        P('이 순서로 말하는 사람은 갈등 중에도 성숙해 보입니다.', 'sub'),
        EN('A three-line formula for any type: name the feeling ("I got tense just now"), own it or set a boundary ("That was my mistake / this bothers me"), propose a next step together ("Next time I\'ll try this. You?").')])),
    slide(8, 'glass', '비교', '\n'.join([
        H2('같은 상황,<br>다른 <em>버전</em>'),
        STEPS([('실수', '구버전 "억울해, 어쩔 수 없었어" → 새 버전 "내 실수야. 다음엔 이렇게"'), ('취향', '구버전 "아무거나" → 새 버전 "난 A가 좋아. B도 열려 있어"')]),
        P('전자는 "아직 자라는 중", 후자는 "같이 미래를 그릴 사람"으로 읽힙니다.'),
        EN('Same moment, different versions. Mistake: "It wasn\'t my fault" vs "My mistake, next time I\'ll do this." Asked your opinion: "Whatever" vs "I\'d like A, but I\'m open to B." One reads as still growing, one as a partner.')])),
    slide(9, 'spot', '주의', '\n'.join([
        H2('상대 방어기제를<br><em>진단</em>하지 마세요'),
        li([('✕', '"너 지금 투사하는 거야"', '분석은 공격으로 들립니다'), ('✕', '"그거 방어기제잖아"', '라벨은 대화를 닫습니다'), ('○', '"내가 먼저 바꿔볼게"', '거울은 따라 움직입니다')]),
        EN('Don\'t diagnose your partner\'s defenses. "You\'re projecting" and "That\'s your defense mechanism" land as attacks and shut the talk down. Change yours first. Mirrors move when you move.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '침묵이 오면 → 견딘다 vs 채운다'), ('2', '틀렸을 때 → 인정 vs 해명'), ('3', '불편할 때 → 말한다 vs 쿨한 척')]),
        '    <div class="rule"></div>',
        P('나를 지키던 방패를<br>이제는 내려놓아도 되는<br>나이가 됐습니다.', 'big'),
        P('여섯 가지 중 내 버전은 몇 번인가요? 댓글로 번호만 남겨주세요.', 'sub'),
        CTA('저장 → 다툰 날 밤에 다시 보기', '사랑받고 자란 사람 구분법'),
        EN('Check: when silence comes, do you sit with it or fill it? When wrong, admit or explain? When uncomfortable, say it or play cool? You\'re old enough now to lower the shield that once kept you safe.')])),
], caption='''회피형이든 불안형이든, "좋은 사람인데 오래 못 간다"는 말을 듣는다면 방어기제를 의심해볼 때입니다.

방어기제는 나쁜 게 아니라 어린 시절에 깔린 낡은 버전입니다.
말로 침묵을 덮거나, 뭐든 괜찮다고 하거나, 쿨한 척하거나, 해명부터 하거나.
지울 필요 없이 세 문장으로 업데이트하세요. 감정 이름 붙이기, 책임과 경계, 함께 다음 수.
단, 상대의 방어기제를 진단하는 데 쓰면 역효과입니다. 내 것부터 바꾸세요.
다음 편은 "사랑받고 자란 사람 구분법"입니다.
여섯 가지 중 내 유형을 댓글로 남겨주세요.

Defense mechanisms aren't flaws, they're outdated survival software. Over-talking, people-pleasing, playing cool, explaining, blaming. Don't delete them. Update with three lines: name the feeling, own it or set a boundary, propose a next step together.

관계를 이해하고 나를 지키기 위한 글입니다.

#방어기제 #애착유형 #연애심리 #불안형 #회피형''')

# ---------------- 12호 ----------------
EPS['12'] = dict(title='사랑받고 자란 사람 구분법', next='부모와 거리두기가 필요한 신호', slides=[
    slide(1, 'sil', '구분법', '\n'.join([
        H1('사랑받고<br>자란 티,<br><em>진짜</em>와<br>가짜'),
        P('사랑스러워 보인다고<br>다 안정형은 아닙니다', 'sub'),
        EN('"Raised with love": how to tell the real thing from the look-alike. Being lovable on the surface doesn\'t mean being secure.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('함께 있으면 좋은데<br>왜 점점 <em>지칠까</em>'),
        P('밝고 사랑스러운 사람이에요.<br>근데 연락, 선물, 이벤트…<br>해줘도 해줘도 모자라대요.<br>제가 부족한 걸까요?', 'quote'),
        P('사랑받고 자란 것과, 사랑을 증명받아야 하는 것은 다릅니다.', 'sub'),
        EN('"They\'re bright and lovable, but texts, gifts, surprises are never enough. Am I failing?" Being raised with love is different from needing love proven over and over.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('사랑에도<br><em>조건</em>이 붙어 있었을까'),
        li([('A', '있는 그대로 받은 사랑', '존재 자체로 충분하다는 감각'), ('B', '조건을 채워야 받은 사랑', '증명해야 사랑받는다는 믿음')]),
        P('B를 넘치게 받으면 겉은 당당한데 속은 늘 확인이 고픕니다.', 'sub'),
        EN('Was the love conditional? Love given as-is builds "I am enough." Love earned by grades, looks or obedience builds "I must prove it." Plenty of the second kind makes someone confident outside, hungry for proof inside.')])),
    slide(4, 'spot', '불안형 패턴', '\n'.join([
        H2('사랑스러운데<br><em>끝이 없다</em>면'),
        li([('·', '연락 간격이 조금만 벌어져도 서운함'), ('·', '선물, 이벤트로 마음을 확인하려 함'), ('·', '이미 많이 줘도 "더"를 원함'), ('·', '받은 것보다 못 받은 것을 기억')]),
        P('그 사람이 나빠서가 아닙니다. 사랑을 "채워야 하는 통장"으로 배운 겁니다.', 'sub'),
        EN('The anxious pattern: hurt by small gaps in texting, checking love through gifts and surprises, wanting more even when given a lot, remembering what\'s missing over what was given. They learned love as a balance to fill.')])),
    slide(5, 'glass', '안정형 패턴', '\n'.join([
        H2('받은 만큼<br><em>돌려줄</em> 줄 안다'),
        li([('·', '받으면 작게라도 꼭 보답'), ('·', '나를 아끼는 만큼 상대도 아낌'), ('·', '서운함을 요구가 아니라 대화로'), ('·', '혼자서도 자기 기분을 회복')]),
        P('소중하게 자란 사람은 "나도 소중하고, 너도 소중하다"를 몸으로 압니다.', 'sub'),
        EN('The secure pattern: always returns something, even small. Cares for you as much as for themselves. Brings hurt as conversation, not demands. Recovers their mood on their own. "I matter, and so do you."')])),
    slide(6, 'lines', '핵심', '\n'.join([
        H2('배경이 아니라<br><em>균형</em>을 보세요'),
        P('유복하게 자랐는지, 귀하게 컸는지는 단서가 아닙니다. 지금 이 관계에서 주고받는 리듬이 단서입니다.'),
        P('데이트 비용을 내가 더 내도, 다른 방식으로 채워진다면 괜찮습니다. 돈도, 시간도, 마음도 나만 빠져나간다면 신호입니다.', 'sub'),
        EN('Look at balance, not background. Wealth or a pampered upbringing tells you nothing. The give-and-take rhythm right now tells you everything. If only you are draining money, time and heart, that\'s the signal.')])),
    slide(7, 'hands', '가장 실용적인 것', '\n'.join([
        H2('만나고 돌아오는 길,<br>내 <em>배터리</em>를 보세요'),
        P('가장 정직한 측정기는 내 몸입니다. 머리는 "좋은 사람이야"라고 해도 몸은 알고 있습니다.'),
        li([('○', '충전돼서 돌아온다 → 균형'), ('✕', '좋았는데 이상하게 녹초 → 기울어짐')]),
        P('일주일만 기록해보세요. 패턴이 보입니다.', 'sub'),
        EN('The most practical test: check your battery on the way home. Your body is the honest meter. Recharged means balance. "It was nice, but I\'m drained" means it\'s tilting. Track it for a week.')])),
    slide(8, 'glass', '나는 어느 쪽', '\n'.join([
        H2('혹시 내가<br><em>그쪽</em>이라면'),
        P('읽다가 뜨끔했다면 괜찮습니다. 알아챈 순간부터 바뀝니다.'),
        li([('1', '받은 것 하나를 매일 말로 꺼내기'), ('2', '서운함은 "해줘"보다 "나 이랬어"로'), ('3', '확인받고 싶을 때 10분 기다려보기')]),
        EN('If this sounds like you: noticing is where change starts. Say one thing you received each day out loud. Turn "do this for me" into "here\'s how I felt." When you crave reassurance, wait ten minutes first.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('이렇게 몰아세우면<br><em>더</em> 불안해집니다'),
        li([('✕', '"넌 받기만 하잖아"', '증명받으려는 마음에 불을 붙입니다'), ('✕', '계산기 꺼내 들기', '사랑을 장부로 만드는 순간 끝입니다'), ('✕', '몰래 거리 두기', '불안형에게 가장 큰 공포입니다')]),
        EN('Don\'t corner them: "You only take" fuels the need for proof; pulling out a ledger turns love into accounting; quietly pulling away triggers their deepest fear. Talk about balance openly instead.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '시간이 갈수록 → 안심 vs 부담'), ('2', '해준 것에 → 보답 vs 더'), ('3', '함께 있으면 → 충전 vs 방전')]),
        '    <div class="rule"></div>',
        P('사랑스러움은 첫인상,<br>균형은 끝인상.', 'big'),
        P('두 개 이상 뒤쪽이라면, 내 배터리부터 지키세요. 당신은 어느 쪽에 더 가까웠나요?', 'sub'),
        CTA('저장 → 지친 날 다시 보기', '부모와 거리두기가 필요한 신호'),
        EN('Check: over time, do you feel reassured or burdened? Do they return what you give or ask for more? Do you recharge or drain together? Lovability is the first impression. Balance is the last.')])),
], caption='''밝고 사랑스러운 연인인데 함께할수록 지친다면, 불안형 애착의 패턴일 수 있습니다.

사랑받고 자랐다는 것과, 사랑을 계속 증명받아야 하는 것은 다릅니다.
배경이 아니라 지금 관계의 균형을 보세요. 받은 만큼 돌려주는지, 함께 있으면 충전되는지.
가장 정직한 측정기는 만나고 돌아오는 길의 내 배터리입니다.
단, 상대를 몰아세우는 데 쓰지 말고 대화의 출발점으로 쓰세요.
다음 편은 "부모와 거리두기가 필요한 신호"입니다.
당신은 어느 쪽에 가까운지 댓글로 남겨주세요.

Being raised with love isn't the same as needing love proven again and again. Ignore background, watch balance: do they give back, and do you leave recharged or drained? Your body is the most honest meter.

관계를 이해하고 나를 지키기 위한 글입니다.

#불안형 #안정형 #애착유형 #연애심리 #연애고민''')

# ---------------- 13호 ----------------
EPS['13'] = dict(title='부모와 거리두기가 필요한 신호', next='외향형 vs 불안형 구분법', slides=[
    slide(1, 'sil', '독립 편', '\n'.join([
        H1('부모와<br><em>거리두기</em><br>필요한<br>신호'),
        P('끊어내는 게 아니라<br>내 자리를 다시 긋는 일', 'sub'),
        EN('Signs you need distance from your parents. Not cutting them off, but redrawing where you stand.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('서른인데도 부모님 전화 한 통에<br><em>무너져요</em>'),
        P('독립한 지 오래인데<br>"결혼은 언제", "그 직장으로"<br>한마디에 하루가 망가져요.<br>연애에도 번지는 것 같고요.', 'quote'),
        P('부모와의 관계는 성인이 돼도 연애의 밑그림으로 남습니다.', 'sub'),
        EN('"I\'m thirty and one call from my parents wrecks my day. \'When will you marry?\' \'That job won\'t do.\' It spills into my dating." The parent bond stays the sketch under every relationship.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('부모 앞의 내가<br>연인 앞의 <em>나</em>가 됩니다'),
        P('인정받으려 애쓰던 아이는 연인 앞에서도 평가를 기다립니다. 간섭을 피하던 아이는 연인의 관심도 침범으로 느낍니다.'),
        P('그래서 연애가 반복해서 같은 데서 꼬인다면, 시작점은 그 전 관계일 수 있습니다.', 'sub'),
        EN('Who you are with your parents becomes who you are with a partner. A child chasing approval waits to be graded. A child dodging control feels a partner\'s care as intrusion. Repeating knots may start there.')])),
    slide(4, 'spot', '신호', '\n'.join([
        H2('이럴 때가<br>거리두기 <em>신호</em>입니다'),
        li([('1', '통화 후 분노나 무기력이 남는다'), ('2', '큰 결정마다 부모 반응부터 상상'), ('3', '칭찬 한마디에 하루가 좌우된다'), ('4', '연인 말에서 부모 목소리가 들린다')]),
        P('두 개 이상이라면 잔소리 수준을 넘어 자존감까지 닿아 있는 겁니다.', 'sub'),
        EN('Signals: anger or numbness lingers after calls; you imagine their reaction before every big decision; one compliment decides your day; you hear their voice in your partner\'s words. Two or more: it has reached self-worth.')])),
    slide(5, 'glass', '오해', '\n'.join([
        H2('거리두기는<br><em>절연</em>이 아닙니다'),
        STEPS([('절연', '관계를 끊는 것. 원망이 남습니다'), ('거리두기', '내 영역의 선을 긋는 것. 관계는 남습니다')]),
        P('부모를 바꾸는 게 목표가 아닙니다. 부모의 말이 내 안에서 울리는 크기를 줄이는 게 목표입니다.'),
        EN('Distance isn\'t disowning. Cutting off ends the bond and leaves resentment. Setting distance draws a line around your space and keeps the bond. The goal isn\'t changing them, it\'s turning down their volume inside you.')])),
    slide(6, 'lines', '경계 문장', '\n'.join([
        H2('선은<br><em>짧고 담담하게</em>'),
        li([('○', '"그 얘기는 제가 정할게요"'), ('○', '"걱정해주셔서 고마워요. 근데 괜찮아요"'), ('○', '"오늘은 여기까지 얘기할게요"')]),
        P('설득하지 마세요. 이해받으려 할수록 다시 평가의 자리로 돌아갑니다. 선은 설명이 아니라 반복으로 지켜집니다.', 'sub'),
        EN('Boundaries, short and calm: "I\'ll decide that one." "Thanks for worrying, but I\'m okay." "Let\'s stop here for today." Don\'t try to convince. Seeking approval puts you back on trial. Boundaries hold by repetition.')])),
    slide(7, 'hands', '가장 실용적인 것', '\n'.join([
        H2('아침 1분,<br>내 목소리부터 <em>먼저</em>'),
        li([('1', '숨 4초 들이쉬고 6초 내쉬기'), ('2', '"나는 부모의 자화상이 아니다"'), ('3', '"나는 내 선택으로 사는 성인이다"'), ('4', '"오늘은 내 방식대로"')]),
        P('하루의 첫 문장을 내가 정하면, 그날 들어오는 남의 문장이 약해집니다. 가슴에 손을 얹고 소리 내서.', 'sub'),
        EN('The most practical step: one minute every morning. Breathe in 4, out 6. Say aloud, hand on chest: "I am not my parents\' portrait." "I live by my own choices." "Today, my way." Your first sentence weakens theirs.')])),
    slide(8, 'glass', '연애에서', '\n'.join([
        H2('연인에게<br>이렇게 <em>말해</em>두세요'),
        P('혼자 감당하면 부모 문제가 연인 문제로 번집니다. 미리 지도를 건네세요.'),
        li([('○', '"부모님 통화 뒤엔 좀 예민해져"'), ('○', '"그땐 해결 말고 옆에만 있어줘"')]),
        P('설명받은 연인은 오해 대신 편이 됩니다.', 'sub'),
        EN('Tell your partner in advance: "I get edgy after calls with my parents. When that happens, don\'t fix it, just stay close." A partner given the map becomes an ally instead of a casualty.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('이건 거리두기가<br>아니라 <em>되돌이표</em>'),
        li([('✕', '통화 때마다 논쟁으로 이기려 하기', '인정받고 싶은 마음의 다른 얼굴'), ('✕', '연인에게 부모 대신 화풀이', '같은 상처를 다른 사람에게'), ('✕', '연락 끊고 죄책감에 다시 매달리기', '선이 아니라 진자 운동')]),
        EN('Not distance, just a loop: trying to win every argument (still craving approval), venting at your partner instead (passing on the wound), cutting contact then rushing back in guilt (a pendulum, not a line).')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '부모 말이 → 잔소리 vs 자존감 타격'), ('2', '대화 후 → 가벼움 vs 분노·무기력'), ('3', '내 선택을 → 내가 vs 눈치 보며')]),
        '    <div class="rule"></div>',
        P('원망이 아니라 경계,<br>단절이 아니라 독립.', 'big'),
        P('가장 어려운 문을 여는 중입니다. 오늘 아침 문장, 당신은 뭐라고 말할 건가요?', 'sub'),
        CTA('저장 → 부모님 통화 전에 다시 보기', '외향형 vs 불안형 구분법'),
        EN('Check: do their words feel like nagging or hit your self-worth? After talks, lighter or angry and numb? Do you choose freely or watch their reaction? Not resentment but boundaries. Not cutting off but growing up.')])),
], caption='''부모님 전화 한 통에 하루가 무너진다면, 불안형이든 회피형이든 연애에도 그 흔적이 남습니다.

부모 앞의 내가 연인 앞의 나가 됩니다.
거리두기는 절연이 아니라 내 영역의 선을 긋는 일입니다. 설득보다 짧고 담담한 문장의 반복으로.
가장 실용적인 건 아침 1분 확언. 하루의 첫 문장을 내가 정하는 것입니다.
단, 학대나 위협이 있는 관계라면 혼자 감당하지 말고 전문가의 도움을 받으세요.
다음 편은 "외향형 vs 불안형 구분법"입니다.
비슷한 상황이라면 댓글이나 DM으로 남겨주세요.

How you are with your parents becomes how you are with a partner. Distance isn't disowning, it's drawing a line around your space. Keep boundary lines short and calm, start each morning with your own sentence, and give your partner the map.

관계를 이해하고 나를 지키기 위한 글입니다.

#애착유형 #연애심리 #불안형 #회피형 #자존감''')

for n, ep in EPS.items():
    open(f'{here}/body_{n}.html', 'w').write(''.join(ep['slides']))
    open(f'{here}/caption_{n}.txt', 'w').write(ep['caption'].strip() + '\n')
    print(n, ep['title'])
import json
json.dump({n: {'title': e['title'], 'next': e['next']} for n, e in EPS.items()}, open(f'{here}/batch_09_13.json', 'w'), ensure_ascii=False)
