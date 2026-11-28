# 24~28호 원고 → body_NN.html, caption_NN.txt 생성
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

# ---------------- 24호 ----------------
EPS['24'] = dict(title='혼란형 애착, 다가오다 밀어내는 이유', next='안정형 연애가 잘 깨지지 않는 이유', slides=[
    slide(1, 'sil', '혼란형', '\n'.join([
        H1('다가오다<br><em>밀어내는</em><br>사람'),
        P('가까워지고 싶은 마음과<br>도망치고 싶은 마음이 동시에', 'sub'),
        EN('Why someone pulls you close and then pushes you away. Disorganized attachment: wanting closeness and wanting to run, at the very same time.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('주말 내내 붙어 있더니<br>월요일엔 <em>읽씹</em>이에요'),
        P('너무 행복하다고 하다가<br>갑자기 숨 막힌다며<br>며칠씩 사라져요.<br>제가 뭘 잘못한 걸까요?', 'quote'),
        P('잘못해서가 아니라, 가까워진 것 자체가 신호였을지 모릅니다.', 'sub'),
        EN('"They say they\'re so happy, then suddenly feel suffocated and vanish for days. What did I do wrong?" Maybe nothing. Getting close may have been the trigger itself.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('변덕이 아니라<br><em>경보가 두 개</em>'),
        P('멀어지면 "버려질 거야", 가까워지면 "다칠 거야". 두 경보가 번갈아 울리니 어느 자리에도 오래 머물지 못합니다.'),
        P('액셀과 브레이크를 함께 밟는 차처럼, 움직일수록 지칩니다.', 'sub'),
        EN('Not mood swings: two alarms. Distance triggers "I\'ll be abandoned." Closeness triggers "I\'ll get hurt." With both ringing, no spot feels safe. Like pressing gas and brake at once.')])),
    slide(4, 'spot', '뿌리', '\n'.join([
        H2('기댈 곳과 피할 곳이<br><em>같았다면</em>'),
        P('어린 시절 위로를 주던 사람이 동시에 겁나는 사람이었다면, 마음은 다가갈지 피할지 하나로 정하지 못합니다.'),
        P('결함이 아니라, 그 시절을 버티게 해준 방식이었습니다.', 'sub'),
        EN('When the place to lean on was also the place to fear. If a caregiver was both comfort and threat, the heart never settled on approach or escape. Not a flaw: a way to survive back then.')])),
    slide(5, 'glass', '신호', '\n'.join([
        H2('연애에서 보이는<br><em>신호</em>들'),
        li([('·', '처음엔 운명, 몇 주 뒤엔 실망'), ('·', '붙잡다가도 다가오면 밀어냄'), ('·', '다툰 뒤 현실감이 흐려짐'), ('·', '"결국 떠날 거잖아"가 입버릇')]),
        P('이 중 여러 개가 겹친다면 성격보다 애착을 먼저 봐야 합니다.', 'sub'),
        EN('Signs in a relationship: "soulmate" turns into disappointment within weeks, pulling you in then pushing back, feeling unreal after fights, and "you\'ll leave eventually" on repeat.')])),
    slide(6, 'lines', '패턴', '\n'.join([
        H2('같은 원을<br><em>계속</em> 돕니다'),
        STEPS([('가까움', '설렘 → 겁 → 거리두기'), ('거리', '안도 → 외로움 → 다시 붙잡기')]),
        P('몇 바퀴 돌고 나면, 둘 다 무엇이 진짜 마음인지 헷갈리기 시작합니다.'),
        EN('The same loop, again and again. Closeness: excitement, fear, distance. Distance: relief, loneliness, reaching back. After a few laps, neither person knows which feeling is real.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('밀어낼 때가<br><em>가장 가까워진</em> 때'),
        P('거리를 두는 순간은 사이가 나빠졌을 때보다, 너무 좋아졌을 때 자주 옵니다. 좋은 날 다음 날이 가장 흔들리는 날입니다.'),
        li([('✕', '"내가 뭘 잘못했지?"'), ('○', '"많이 가까워져서 겁났구나"')]),
        EN('The twist: the push often comes right after things got really good, not bad. The day after a great day is the shakiest. Not "What did I do wrong?" but "We got close, and that felt scary."')])),
    slide(8, 'glass', '곁에서', '\n'.join([
        H2('곁에 있는 사람이<br>할 수 있는 <em>것</em>'),
        li([('○', '좋은 날 다음엔 속도 늦추기'), ('○', '사라져도 "기다릴게" 한 줄만'), ('○', '사라진 이유를 캐묻지 않기'), ('○', '내 일상과 감정은 내가 지키기')]),
        EN('What a partner can do: slow down after a great day, send one line like "I\'ll be here" when they vanish, don\'t interrogate the reason, and keep your own routine and feelings intact.')])),
    slide(9, 'spot', '주의', '\n'.join([
        H2('이건 혼자<br><em>감당하지</em> 마세요'),
        li([('✕', '위협이나 극단적인 말이 반복될 때', '혼자 버틸 일이 아니라 전문가와 다룰 일입니다'), ('✕', '내가 다 받아주면 낫겠지', '구해주는 게 아니라 곁을 지키는 것까지만'), ('✕', '"너 혼란형이지?" 진단하기', '이름표보다 반복되는 행동을 함께 보기')]),
        EN('Don\'t carry these alone: repeated threats or extreme words need professional help. "If I accept everything, they\'ll heal" isn\'t your job. And don\'t label them; look at the repeated behavior together.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '좋은 날 다음 → 편안 vs 도망'), ('2', '다투고 나면 → 대화 vs 증발'), ('3', '관계를 보면 → 기대 vs "결국 끝"')]),
        '    <div class="rule"></div>',
        P('밀어낸다고<br>마음이 없는 건 아니다.', 'big'),
        P('좋은 날 다음에 더 불안해지나요? 댓글로 예/아니오만 남겨주세요.', 'sub'),
        CTA('저장 → 마음이 오락가락할 때 다시 보기', '안정형 연애가 잘 깨지지 않는 이유'),
        EN('Check: after a good day, calm or escape? After a fight, talk or vanish? Looking ahead, hope or "it\'ll end anyway"? A push doesn\'t always mean no feeling.')])),
], caption='''애착유형 중 혼란형은 왜 다가왔다가 갑자기 밀어낼까요? 가장 헷갈리는 이 패턴에는 이유가 있습니다.

혼란형 안에는 경보가 두 개 있습니다. 멀어지면 "버려질 거야", 가까워지면 "다칠 거야".
그래서 거리를 두는 순간은 사이가 나빠졌을 때보다 너무 좋아졌을 때 더 자주 옵니다.
곁에 있는 사람은 캐묻기보다 속도를 늦추고, 자기 일상을 지키는 게 먼저입니다.
단, 위협이나 극단적인 말이 반복된다면 혼자 감당하지 말고 전문가의 도움을 받으세요.
다음 편은 "안정형 연애가 잘 깨지지 않는 이유"입니다.
가까워질수록 겁났던 순간이 있다면 댓글이나 DM으로 들려주세요.

Disorganized attachment runs on two alarms: distance feels like abandonment, closeness feels like danger. The push often comes right after a good day. Slow down, don't interrogate, and protect your own life.

관계를 이해하고 나를 지키기 위한 글입니다.

#혼란형 #애착유형 #불안형 #회피형 #연애심리''')

# ---------------- 25호 ----------------
EPS['25'] = dict(title='안정형 연애가 잘 깨지지 않는 이유', next='실패하지 않는 연애 공식', slides=[
    slide(1, 'sil', '안정형', '\n'.join([
        H1('쉽게<br><em>안 깨지는</em><br>연애의<br>비밀'),
        P('특별한 기술이 아니라<br>무게중심이 다릅니다', 'sub'),
        EN('Why secure relationships rarely break. It isn\'t a special technique. Their center of gravity is simply in a different place.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('싸워도 다음 날<br>그냥 <em>괜찮은</em> 커플'),
        P('친구 커플은 싸워도<br>다음 날 아무렇지 않아요.<br>우리는 한 번 싸우면<br>일주일이 지옥인데요.', 'quote'),
        P('차이는 다툼의 횟수가 아니라, 다툰 뒤 돌아오는 속도입니다.', 'sub'),
        EN('"My friends fight and are fine the next day. One fight and we\'re in hell for a week." The difference isn\'t how often you fight. It\'s how fast you come back.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('안 싸워서가 아니라<br><em>돌아와서</em>입니다'),
        P('안정형 커플도 다툽니다. 다만 다툼을 관계의 끝으로 읽지 않습니다. 문제는 문제일 뿐, 둘 사이에 내려진 판결이 아니니까요.'),
        P('흔들려도 제자리로 오는 건, 무게중심이 아래에 있어서입니다.', 'sub'),
        EN('Not because they never fight, but because they return. Secure couples argue too; they just don\'t read a fight as the end. A problem is a problem, not a verdict. Low center of gravity, quick to right itself.')])),
    slide(4, 'spot', '핵심', '\n'.join([
        H2('무게중심은<br><em>두 개의 믿음</em>'),
        li([('1', '나는 사랑받아도 되는 사람'), ('2', '상대도 기본은 믿어도 되는 사람')]),
        P('하나만 있으면 기울어집니다. 나만 믿으면 독선이 되고, 상대만 믿으면 매달림이 됩니다.'),
        EN('The center of gravity is two beliefs: "I deserve love" and "My partner is mostly trustworthy." With only one, you tilt: trusting only yourself becomes rigidity; trusting only them becomes clinging.')])),
    slide(5, 'glass', '이유 1', '\n'.join([
        H2('답장이 늦어도<br><em>이야기</em>를 안 지어요'),
        P('연락이 뜸한 날, 안정형은 "바쁜가 보다"에서 멈춥니다. 빈칸에 최악의 시나리오를 채워 넣지 않습니다.'),
        P('빈칸을 빈칸으로 두는 힘이 관계를 지킵니다.', 'sub'),
        EN('Reason 1: a late reply doesn\'t become a story. On a quiet day they stop at "must be busy" and don\'t fill the blank with worst cases. Leaving a blank as a blank protects the relationship.')])),
    slide(6, 'lines', '이유 2', '\n'.join([
        H2('다툼의 주어가<br><em>"우리"</em>입니다'),
        STEPS([('불안정', '"너 때문에 이렇게 됐잖아"'), ('안정', '"우리 이거 어떻게 풀까?"')]),
        P('상대를 이겨야 할 사람이 아니라, 같은 문제를 함께 마주 본 사람으로 둡니다.'),
        EN('Reason 2: the subject of the fight is "we." Insecure: "Look what you did." Secure: "How do we sort this out?" Your partner isn\'t someone to beat, but someone facing the same problem with you.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('맞지 않으면<br><em>빨리</em> 내려놓습니다'),
        P('안정형이 오래가는 건 아무하고나 버텨서가 아닙니다. 처음부터 아니다 싶은 사람 곁에 오래 머물지 않기 때문입니다.'),
        P('잘 버티는 것보다 잘 고르는 게 먼저입니다.', 'sub'),
        EN('The twist: they let go early when it doesn\'t fit. Secure relationships last not because they endure anyone, but because they don\'t linger with the wrong person. Choosing well comes before holding on.')])),
    slide(8, 'glass', '이유 3', '\n'.join([
        H2('원하는 걸<br><em>처음부터</em> 말해요'),
        li([('○', '"나는 연락이 자주 오는 게 좋아"'), ('○', '"아까 그 말은 좀 서운했어"'), ('○', '"이번 주는 혼자 쉬고 싶어"')]),
        P('숨기고 맞춰주다 한 번에 터지는 대신, 작을 때 꺼냅니다.'),
        EN('Reason 3: they say what they want from the start. "I like hearing from you often." "That comment stung a bit." "I need a quiet week alone." Small and early, instead of hiding it until it explodes.')])),
    slide(9, 'spot', '오해', '\n'.join([
        H2('안정형에 대한<br><em>오해</em> 세 가지'),
        li([('✕', '타고나야만 될 수 있다', '관계 속에서 배워서 갖출 수 있습니다'), ('✕', '안정형 연애는 설렘이 없다', '설렘이 불안 대신 편안함 위에 섭니다'), ('✕', '무엇이든 다 참아준다', '선을 넘으면 오히려 가장 단호합니다')]),
        EN('Three myths: you must be born secure (it can be learned in relationships), secure love has no spark (the spark stands on ease, not anxiety), they tolerate anything (cross the line and they\'re the firmest).')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '다툰 다음 날 → 회복 vs 냉전'), ('2', '답장 늦으면 → 빈칸 vs 시나리오'), ('3', '서운할 때 → 바로 말 vs 쌓기')]),
        '    <div class="rule"></div>',
        P('안 흔들리는 게 아니라<br>돌아오는 것.', 'big'),
        P('다툰 뒤 회복까지 보통 며칠 걸리나요? 댓글로 알려주세요.', 'sub'),
        CTA('저장 → 다툰 다음 날 다시 보기', '실패하지 않는 연애 공식'),
        EN('Check: the day after a fight, repair or cold war? A late reply, a blank or a script? When hurt, say it now or stockpile it? Security isn\'t never shaking. It\'s coming back.')])),
], caption='''안정형 커플은 왜 싸워도 다음 날 괜찮을까요? 안정형 애착의 연애가 잘 깨지지 않는 데는 분명한 이유가 있습니다.

안 싸워서가 아니라, 다툼을 관계의 끝으로 읽지 않고 빨리 돌아오기 때문입니다.
답장이 늦어도 빈칸에 이야기를 지어내지 않고, 다툼의 주어를 "우리"로 둡니다.
그리고 맞지 않는 사람 곁에는 처음부터 오래 머물지 않습니다.
단, 안정형은 타고나는 것만이 아닙니다. 관계 속에서 배워서 갖출 수 있습니다.
다음 편은 "실패하지 않는 연애 공식"입니다.
다툰 뒤 회복까지 며칠이 걸리는지 댓글이나 DM으로 남겨주세요.

Secure couples fight too. They just come back faster: no stories in the blanks, "we" as the subject of every fight, and early exits from the wrong person. Security can be learned.

관계를 이해하고 나를 지키기 위한 글입니다.

#안정형 #애착유형 #불안형 #건강한연애 #연애심리''')

# ---------------- 26호 ----------------
EPS['26'] = dict(title='실패하지 않는 연애 공식', next='ISTJ의 연애, 말보다 약속', slides=[
    slide(1, 'sil', '공식', '\n'.join([
        H1('실패<br>안 하는<br><em>연애</em><br>공식'),
        P('기술보다 먼저 필요한 건<br>나를 아는 일입니다', 'sub'),
        EN('A relationship formula that doesn\'t fail. Before any technique, you need one thing first: knowing yourself.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('맞춰줄수록<br><em>멀어지는</em> 이유'),
        P('그 사람 취향 따라<br>음악도 옷도 바꿨는데<br>오히려 질린대요.<br>뭘 더 해야 하죠?', 'quote'),
        P('더 하는 게 아니라, 나를 덜 지워야 합니다.', 'sub'),
        EN('"I changed my music and clothes to match their taste, and now they say they\'re bored. What more should I do?" Not more. Erase less of yourself.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('나를 지우면<br>매력도 <em>지워집니다</em>'),
        P('상대가 좋아할 모습으로 바꿀수록, 상대는 누구와 연애하는지 모르게 됩니다. 사람은 복사본보다 원본에 끌립니다.'),
        P('공식의 첫 줄은 상대가 아니라 나입니다.', 'sub'),
        EN('Erase yourself and your appeal goes with it. The more you reshape yourself for them, the less they know who they\'re dating. People fall for originals, not copies. Line one of the formula is you.')])),
    slide(4, 'spot', '0단계', '\n'.join([
        H2('시작 전에<br>세 가지 <em>질문</em>'),
        li([('1', '나는 언제 가장 나다운가'), ('2', '내 약점을 숨기지 않고 말할 수 있나'), ('3', '내 필요를 미안해하지 않나')]),
        P('셋 다 "응"이 나오면, 그다음부터가 공식입니다.', 'sub'),
        EN('Step 0, three questions: When am I most myself? Can I name my weaknesses without hiding them? Do I state my needs without apologizing? Three yeses, and the formula can begin.')])),
    slide(5, 'glass', '1단계', '\n'.join([
        H2('1단계,<br><em>편안함</em>으로 문 열기'),
        P('처음엔 닮은 점이 마음을 엽니다. 억지로 맞춘 취미 말고, 원래 둘 다 아끼던 것을 찾습니다.'),
        li([('·', '약속 시간을 대하는 감각'), ('·', '쉬는 날을 보내는 방식'), ('·', '일과 돈, 가족을 대하는 태도')]),
        EN('Step 1: open the door with ease. Shared ground opens hearts first. Not hobbies you fake, but things you both already value: how you treat time, how you spend days off, how you see work, money, family.')])),
    slide(6, 'lines', '2단계', '\n'.join([
        H2('2단계,<br>몰랐던 <em>면</em> 보여주기'),
        P('편안함만 있으면 친구로 머뭅니다. 상대가 예상 못 한 나의 다른 면이 호기심을 깨웁니다. 연기가 아니라 원래 있던 면이어야 합니다.'),
        STEPS([('평소', '일정표대로 움직이는 사람'), ('의외', '"오늘은 그냥 걷다 정하자"')]),
        EN('Step 2: show a side they didn\'t expect. Ease alone keeps you friends; a surprising side sparks curiosity. It must be real, not acted. Usually: runs on a schedule. Surprise: "Let\'s just walk and decide."')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('3단계는<br><em>여백</em>과 <em>특별함</em>'),
        P('내 시간이 따로 있는 사람인데, 그 시간을 너에게 기꺼이 쓴다는 것. 이 둘이 함께 보일 때 관계가 한 칸 나아갑니다.'),
        li([('·', '"이번 주말엔 혼자 산에 다녀올게"'), ('·', '"그래도 금요일 저녁은 비워뒀어"')]),
        EN('The twist, step 3: space plus specialness. Someone with a life of their own who still gladly gives you their time. "I\'m hiking solo this weekend." "But I kept Friday night free for you."')])),
    slide(8, 'glass', '태도', '\n'.join([
        H2('증명하는 연애,<br><em>보여주는</em> 연애'),
        STEPS([('증명', '"이래야 날 좋아하겠지"'), ('표현', '"이게 나야, 궁금하면 와"')]),
        P('증명은 상대의 반응에 매달리게 하고, 보여주기는 나를 중심에 둡니다.'),
        EN('Proving versus showing. Proving: "They\'ll like me only if I\'m like this." Showing: "This is me. Come closer if you\'re curious." Proving ties you to their reaction; showing keeps you centered.')])),
    slide(9, 'spot', '금지', '\n'.join([
        H2('공식이<br><em>꼼수</em>가 되는 순간'),
        li([('✕', '없는 취미를 있는 척', '들키는 순간 신뢰가 먼저 무너집니다'), ('✕', '일부러 연락 끊고 애태우기', '여백은 전략이 아니라 생활입니다'), ('✕', '여러 명에게 같은 "특별함"', '특별함은 한 사람에게만 진짜입니다')]),
        EN('When the formula becomes a trick: faking hobbies (trust breaks when found out), going silent on purpose (space is a life, not a tactic), giving several people the same "special" treatment.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '상대 앞에서 → 원본 vs 복사본'), ('2', '닮은 점 → 원래 vs 억지'), ('3', '내 시간 → 있음 vs 전부 너')]),
        '    <div class="rule"></div>',
        P('맞추는 사람보다<br>보여주는 사람.', 'big'),
        P('연애할 때 가장 많이 지웠던 내 모습은 뭔가요? 댓글로 남겨주세요.', 'sub'),
        CTA('저장 → 또 맞추고 있을 때 다시 보기', 'ISTJ의 연애, 말보다 약속'),
        EN('Check: with them, are you the original or a copy? Is shared ground real or forced? Do you still have your own time, or is it all theirs? Be someone who shows, not someone who matches.')])),
], caption='''불안형처럼 상대에게 맞추다 지치는 연애라면, 실패하지 않는 연애 공식의 첫 줄부터 다시 써야 합니다.

공식의 시작은 상대가 아니라 나입니다. 나를 지울수록 매력도 함께 지워집니다.
1단계는 원래 닮은 점에서 오는 편안함, 2단계는 몰랐던 나의 다른 면입니다.
3단계는 여백과 특별함입니다. 내 시간이 있는 사람이 그 시간을 기꺼이 상대에게 쓰는 것.
단, 없는 취미를 꾸미거나 일부러 애태우는 순간 공식은 꼼수가 됩니다.
다음 편은 "ISTJ의 연애, 말보다 약속"입니다.
연애할 때 가장 많이 지웠던 내 모습을 댓글이나 DM으로 들려주세요.

The formula starts with you, not them. Ease from real shared values, a side they didn't expect, then space plus specialness. The moment you fake it, the formula becomes a trick.

관계를 이해하고 나를 지키기 위한 글입니다.

#연애공식 #불안형 #애착유형 #연애심리 #건강한연애''')

# ---------------- 27호 ----------------
EPS['27'] = dict(title='ISTJ의 연애, 말보다 약속', next='ISFJ의 연애, 기억으로 하는 사랑', slides=[
    slide(1, 'sil', 'ISTJ', '\n'.join([
        H1('ISTJ의<br>사랑은<br><em>약속</em>으로<br>말한다'),
        P('표현이 적다고<br>마음까지 적은 건 아닙니다', 'sub'),
        EN('ISTJ love speaks through promises kept. Fewer words of affection don\'t mean less feeling.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('좋아한다는 말은 없는데<br><em>전화는 꼭</em> 와요'),
        P('사랑한다는 말은<br>거의 안 해요.<br>그런데 퇴근길엔<br>꼭 전화가 와요.', 'quote'),
        P('말 대신 반복으로 마음을 전하는 사람이 있습니다.', 'sub'),
        EN('"They almost never say I love you. But on the way home from work, they always call." Some people say it through repetition instead of words.')])),
    slide(3, 'lines', '핵심', '\n'.join([
        H2('이들에게 사랑은<br><em>반복</em>되는 행동'),
        P('한 번의 큰 이벤트보다 매주 같은 요일의 저녁이 더 진심입니다. 같은 일을 같은 방식으로 계속하는 것, 그게 이들의 고백입니다.'),
        P('달력에 적힌 약속이 이들의 연애편지입니다.', 'sub'),
        EN('For them, love is a repeated action. The same weeknight dinner means more than one big event. Doing the same thing the same way, again and again, is their confession. Their calendar is a love letter.')])),
    slide(4, 'spot', '특징', '\n'.join([
        H2('연애할 때<br>보이는 <em>모습</em>'),
        li([('·', '한 말은 지키고, 못 지킬 말은 안 함'), ('·', '기념일과 취향을 정확히 기억함'), ('·', '천천히 열고, 한번 열면 오래 감'), ('·', '문제 앞에선 감정보다 해결부터')]),
        EN('What it looks like: they keep what they say and won\'t promise what they can\'t. They remember dates and preferences precisely, open slowly but stay long, and go for solutions before feelings.')])),
    slide(5, 'glass', '속도', '\n'.join([
        H2('천천히 열리는<br><em>이유</em>'),
        P('이들은 지나온 경험을 기준으로 사람을 봅니다. 믿을 만하다는 기록이 쌓여야 문이 열립니다. 느린 게 아니라 확인 중인 겁니다.'),
        P('재촉하면 확인 기간이 오히려 길어집니다.', 'sub'),
        EN('Why they open slowly: they judge by past experience. The door opens once enough evidence of trust has piled up. They aren\'t slow; they\'re verifying. Rushing them only extends the check.')])),
    slide(6, 'lines', '오해', '\n'.join([
        H2('무뚝뚝함 뒤의<br><em>진짜</em> 얼굴'),
        STEPS([('겉', '"무뚝뚝하다, 계산적이다"'), ('속', '"책임질 수 있는 말만 한다"')]),
        P('마음을 말로 꺼내는 데 시간이 걸립니다. 대신 한번 꺼낸 마음은 쉽게 바뀌지 않습니다.'),
        EN('The real face behind the bluntness. Outside: "cold, calculating." Inside: "I only say what I can stand behind." Putting feelings into words takes time, but once said, they rarely change.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('침착한 사람의<br><em>숨은</em> 불안'),
        P('평소엔 차분해도 계획이 크게 틀어지면 "이러다 다 무너지면 어쩌지" 하는 걱정이 한꺼번에 몰려옵니다.'),
        P('이때 필요한 건 위로의 말보다 "다음엔 이렇게 하자"는 구체적인 계획입니다.', 'sub'),
        EN('The twist: calm people carry hidden worry. When plans fall apart, "Is this all going to end?" can flood in at once. What helps most isn\'t comfort words but a concrete "Next time, let\'s do this."')])),
    slide(8, 'glass', '통하는 말', '\n'.join([
        H2('곁에서<br><em>통하는</em> 말'),
        li([('○', '"그때 약속 지켜줘서 고마웠어"'), ('○', '바뀐 일정은 미리, 이유와 함께'), ('○', '서운함은 구체적인 장면으로'), ('○', '감정 표현을 재촉하지 않기')]),
        EN('What works with them: "Thank you for keeping that promise." Share schedule changes early, with a reason. Describe hurt through a specific scene. Don\'t push them to express feelings on demand.')])),
    slide(9, 'spot', '주의', '\n'.join([
        H2('성실함이<br><em>숨 막힘</em>이 될 때'),
        li([('✕', '챙긴 만큼 돌려받길 기대', '챙김이 거래가 되면 사랑이 아니라 장부'), ('✕', '자기 방식만 정답으로', '규칙은 함께 정할 때만 둘의 것입니다'), ('✕', '감정 이야기는 늘 나중으로', '미룬 마음은 이자처럼 불어납니다')]),
        EN('When diligence turns stifling: expecting care to be paid back (a ledger, not love), treating their way as the only way (rules belong to both only if made together), always postponing feelings.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '사랑 표현 → 말 vs 반복'), ('2', '여는 속도 → 재촉 vs 기다림'), ('3', '흔들릴 때 → 위로 vs 계획')]),
        '    <div class="rule"></div>',
        P('말이 적은 사람은<br>약속으로 말한다.', 'big'),
        P('내 곁의 ISTJ는 어떻게 사랑을 표현하나요? 댓글로 알려주세요.', 'sub'),
        CTA('저장 → 표현이 아쉬운 날 다시 보기', 'ISFJ의 연애, 기억으로 하는 사랑'),
        EN('Check: is love shown in words or repetition? Do you rush them open or wait? When shaken, do they need comfort or a plan? People of few words speak through promises kept.')])),
], caption='''무뚝뚝해 보이는 ISTJ의 연애, 애착유형보다 먼저 보이는 건 "약속"입니다.

한 번의 큰 이벤트보다 매주 같은 요일의 저녁, 지켜진 약속 하나가 이들의 고백입니다.
믿을 만한 기록이 쌓여야 마음이 열리기 때문에, 느린 게 아니라 확인 중인 겁니다.
계획이 크게 틀어질 땐 숨은 걱정이 몰려옵니다. 이때는 위로보다 구체적인 다음 계획이 통합니다.
단, MBTI는 성향일 뿐입니다. 같은 ISTJ라도 안정형일 때와 불안할 때의 모습은 다릅니다.
다음 편은 "ISFJ의 연애, 기억으로 하는 사랑"입니다.
내 곁의 ISTJ가 사랑을 표현하는 방식을 댓글이나 DM으로 알려주세요.

ISTJs say love through repetition and promises kept. They open slowly because they verify trust. When plans collapse, a concrete next step helps more than comfort. MBTI is a tendency, not a verdict.

관계를 이해하고 나를 지키기 위한 글입니다.

#ISTJ #MBTI연애 #애착유형 #안정형 #연애심리''')

# ---------------- 28호 ----------------
EPS['28'] = dict(title='ISFJ의 연애, 기억으로 하는 사랑', next='INFJ의 연애, 마음의 깊이부터', slides=[
    slide(1, 'sil', 'ISFJ', '\n'.join([
        H1('ISFJ는<br><em>기억</em>으로<br>사랑한다'),
        P('지나가듯 한 말까지<br>챙겨 오는 사람의 연애', 'sub'),
        EN('ISFJs love through memory. What dating looks like with someone who remembers even the things you mentioned in passing.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('말한 적도 없는데<br><em>기억</em>하고 있었어요'),
        P('지나가듯 말한<br>좋아하는 과자를<br>석 달 뒤에 사 왔어요.<br>원래 이런 사람인가요?', 'quote'),
        P('네. 이들에게 기억은 가장 조용한 고백입니다.', 'sub'),
        EN('"I mentioned my favorite snack once, in passing. Three months later they showed up with it. Are they always like this?" Yes. For them, remembering is the quietest way to confess.')])),
    slide(3, 'lines', '핵심', '\n'.join([
        H2('챙김이<br><em>사랑의 언어</em>'),
        P('이들은 상대의 작은 취향을 마음속 서랍에 차곡차곡 넣어둡니다. 필요한 순간 꺼내 건네는 것, 그게 이들의 "좋아해"입니다.'),
        P('서랍이 가득할수록 마음도 깊습니다.', 'sub'),
        EN('Care is their love language. They file away your small preferences in a mental drawer and pull one out right when you need it. That\'s how they say "I like you." A full drawer means a deep heart.')])),
    slide(4, 'spot', '특징', '\n'.join([
        H2('연애할 때<br>보이는 <em>모습</em>'),
        li([('·', '상대 컨디션 변화를 먼저 알아챔'), ('·', '갈등보다 분위기를 먼저 지킴'), ('·', '부탁을 잘 거절하지 못함'), ('·', '고맙다는 말에 가장 힘이 남')]),
        EN('What it looks like: they notice your mood shifts first, protect the atmosphere before addressing conflict, find it hard to say no, and are recharged most by hearing "thank you."')])),
    slide(5, 'glass', '속마음', '\n'.join([
        H2('"괜찮아"의<br><em>진짜</em> 뜻'),
        P('분위기를 깨기 싫어 "괜찮아"를 먼저 꺼냅니다. 그런 괜찮음이 쌓이면, 어느 날 조용히 마음의 문을 닫기도 합니다.'),
        P('조용한 사람일수록 서운함은 소리 없이 쌓입니다.', 'sub'),
        EN('What "I\'m fine" really means. They say it to keep the peace. When those "fines" pile up, one day they may quietly close the door. The quieter the person, the more silently hurt accumulates.')])),
    slide(6, 'lines', '균형', '\n'.join([
        H2('헌신에도<br><em>적정 온도</em>가 있어요'),
        STEPS([('건강', '"네가 편하면 나도 좋아"'), ('과열', '"내가 다 할게, 넌 몰라도 돼"')]),
        P('챙김이 넘치면 상대는 받기만 하는 사람이 되고, 이들은 조용히 지쳐갑니다.'),
        EN('Devotion has a healthy temperature. Healthy: "If you\'re comfortable, so am I." Overheated: "I\'ll handle it all, you don\'t need to know." Too much care makes the partner a receiver and wears them out.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('이들에게 필요한 건<br><em>받는 연습</em>'),
        P('늘 주는 쪽이라 받는 데 서툽니다. 챙김을 받으면 미안해하고, 갚을 방법부터 찾습니다.'),
        P('가장 큰 선물은 "그냥 받아도 돼"라는 한마디입니다.', 'sub'),
        EN('The twist: what they need is practice receiving. Always the giver, they\'re clumsy at taking. Cared for, they feel sorry and look for a way to repay. The best gift: "You can just accept it."')])),
    slide(8, 'glass', '통하는 말', '\n'.join([
        H2('곁에서<br><em>통하는</em> 말'),
        li([('○', '"그걸 기억해줬어? 고마워"'), ('○', '"괜찮다 해도 한 번 더 물어볼게"'), ('○', '작은 챙김을 먼저 돌려주기'), ('○', '다툰 뒤 "우리 괜찮아"를 말로')]),
        EN('What works: "You remembered that? Thank you." "Even if you say you\'re fine, I\'ll ask once more." Return small acts of care first. After an argument, say "We\'re okay" out loud.')])),
    slide(9, 'spot', '주의', '\n'.join([
        H2('다정함이<br><em>무거워질</em> 때'),
        li([('✕', '고마움을 당연하게 여기기', '당연해지는 순간 서랍이 닫힙니다'), ('✕', '"넌 착하니까 이해하지?"', '착함에 기대면 신뢰가 깎입니다'), ('✕', '혼자 참다 한 번에 끊기', '쌓기 전에 작게 꺼내는 연습을')]),
        EN('When kindness gets heavy: taking their care for granted (the drawer closes), "You\'re nice, so you\'ll understand, right?" (leaning on kindness erodes trust), and enduring silently, then cutting off at once.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '챙김을 받으면 → 고마움 vs 당연'), ('2', '"괜찮아" 뒤엔 → 질문 vs 넘김'), ('3', '서운함은 → 작게 vs 한꺼번에')]),
        '    <div class="rule"></div>',
        P('기억해주는 사람을<br>기억할 것.', 'big'),
        P('누군가 내 사소한 말을 기억해준 순간, 있었나요? 댓글로 들려주세요.', 'sub'),
        CTA('저장 → 챙김이 당연해질 때 다시 보기', 'INFJ의 연애, 마음의 깊이부터'),
        EN('Check: when cared for, gratitude or taking it for granted? After "I\'m fine," a follow-up question or moving on? Hurt shared small, or all at once? Remember the one who remembers.')])),
], caption='''ISFJ의 연애, 애착유형과 상관없이 가장 먼저 보이는 건 "기억"입니다. 지나가듯 한 말까지 챙겨 오는 사람이니까요.

이들은 상대의 작은 취향을 마음속 서랍에 넣어두었다가 필요한 순간 꺼내 건넵니다. 그게 이들의 "좋아해"입니다.
분위기를 지키려고 "괜찮아"를 먼저 말하지만, 그 괜찮음이 쌓이면 조용히 문을 닫기도 합니다.
늘 주는 쪽이라 받는 데 서툽니다. 가장 큰 선물은 "그냥 받아도 돼"라는 한마디입니다.
단, MBTI는 성향일 뿐입니다. 같은 ISFJ라도 안정형일 때와 지쳤을 때의 모습은 다릅니다.
다음 편은 "INFJ의 연애, 마음의 깊이부터"입니다.
누군가 내 사소한 말을 기억해준 순간을 댓글이나 DM으로 들려주세요.

ISFJs love through memory and quiet care. Their "I'm fine" can hide hurt that piles up silently. They need practice receiving. MBTI is a tendency; how someone loves also depends on their attachment state.

관계를 이해하고 나를 지키기 위한 글입니다.

#ISFJ #MBTI연애 #애착유형 #안정형 #연애심리''')

for n, ep in EPS.items():
    open(f'{here}/body_{n}.html', 'w').write(''.join(ep['slides']))
    open(f'{here}/caption_{n}.txt', 'w').write(ep['caption'].strip() + '\n')
    print(n, ep['title'])
import json
json.dump({n: {'title': e['title'], 'next': e['next']} for n, e in EPS.items()}, open(f'{here}/batch_24_28.json', 'w'), ensure_ascii=False)
