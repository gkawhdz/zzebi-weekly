# 19~23호 원고 → body_NN.html, caption_NN.txt 생성
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

# ---------------- 19호 ----------------
EPS['19'] = dict(title='퀀텀점프 원리: 관계가 한 번에 바뀌는 순간', next='5분 저널링으로 감정 정리하는 법', slides=[
    slide(1, 'sil', '원리', '\n'.join([
        H1('관계가<br>한 번에<br><em>바뀌는</em><br>순간'),
        P('어느 날 갑자기 달라진 것 같지만<br>사실은 조용히 쌓인 결과입니다', 'sub'),
        EN('The moment a relationship shifts all at once. It looks sudden, but it is the result of quiet changes stacking up underneath.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('결심은 백 번,<br>변한 건 <em>없어요</em>'),
        P('이번엔 안 흔들리겠다고<br>매번 다짐하는데<br>답장 하나에 또<br>원래대로 돌아가요.', 'quote'),
        P('다짐이 모자란 게 아닙니다. 순서가 빠졌을 뿐입니다.', 'sub'),
        EN('"I swear every time I won\'t get shaken, then one late reply and I\'m back to square one." It\'s not weak willpower. A step in the order is missing.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('급하게 바꾸려 할수록<br>더 세게 <em>되돌아옵니다</em>'),
        P('하루아침에 딴사람이 되려 하면 몸이 먼저 버팁니다. 익숙한 패턴은 불편해도 "아는 길"이라 편하게 느껴지니까요.'),
        P('그래서 결심은 사흘을 못 갑니다.', 'sub'),
        EN('The harder you force change, the harder you snap back. Try to become someone new overnight and you resist. Even an uncomfortable pattern feels like familiar ground. That\'s why resolutions fade in three days.')])),
    slide(4, 'spot', '핵심', '\n'.join([
        H2('99도까지는<br>아무 일도 <em>없어 보입니다</em>'),
        P('물은 99도까지 조용하다가 100도에서 끓습니다. 관계도 같습니다. 작은 관찰이 쌓이다 어느 순간 반응이 통째로 바뀝니다.'),
        P('퀀텀점프는 기적이 아니라 끓는점입니다.', 'sub'),
        EN('Nothing seems to happen until 99°C. Water stays still, then boils at 100. Relationships work the same way: small observations pile up until reactions change at once. A boiling point, not a miracle.')])),
    slide(5, 'glass', '1단계', '\n'.join([
        H2('먼저, 나를<br><em>정확히</em> 보기'),
        P('그날의 기분 말고 반복을 봅니다. 어떤 순간에 불안해지고, 그때 무엇을 하는지.'),
        li([('·', '반복되는 다툼의 첫 장면'), ('·', '유독 크게 흔들리는 말 한마디'), ('·', '그 직후 내가 하는 행동')]),
        EN('Step 1: see yourself clearly. Look at patterns, not just feelings: the opening scene of repeated fights, the one phrase that shakes you most, and what you do right after.')])),
    slide(6, 'lines', '2단계', '\n'.join([
        H2('감정에 타지 말고<br><em>지켜보기</em>'),
        P('감정이 올라와도 바로 반응하지 않고, 한 발 뒤에서 바라봅니다. "지금 서운함이 7쯤 올라왔네."'),
        STEPS([('버릇', '불안 → 바로 연락 폭탄'), ('멈춤', '불안 → 알아차림 → 고르기')]),
        EN('Step 2: watch the feeling instead of riding it. Step back and notice: "Hurt is at about a 7 right now." Habit: anxiety → message flood. Pause: anxiety → notice → decide.')])),
    slide(7, 'hands', '실전 팁', '\n'.join([
        H2('깨달음은 <em>적어야</em><br>내 것이 됩니다'),
        P('머릿속 다짐은 다음 날 흐려집니다. 한 줄이라도 글로 남기면, 생각은 다시 꺼내 볼 수 있는 기록이 됩니다.'),
        P('"이 상황에선 이렇게 한다" 한 문장이 점프대입니다.', 'sub'),
        EN('Most practical tip: insight sticks only once it\'s written. Mental promises blur by morning. One written line is something you can return to. "In this situation, I do this" is your springboard.')])),
    slide(8, 'glass', '3단계', '\n'.join([
        H2('배운 것을<br>나의 <em>기준</em>으로'),
        P('같은 깨달음이 세 번 반복되면, 그건 내 원칙이 될 준비가 된 겁니다.'),
        li([('○', '"연락이 늦어도 내 가치는 그대로"'), ('○', '"서운하면 그날 안에 말한다"'), ('○', '"침묵으로 벌주지 않는다"')]),
        EN('Step 3: turn lessons into rules. When an insight repeats three times, it\'s ready to be a principle: "A late reply doesn\'t lower my worth." "I say I\'m hurt the same day." "No silent punishment."')])),
    slide(9, 'spot', '함정', '\n'.join([
        H2('이러면 끓기 직전에<br><em>불을 끕니다</em>'),
        li([('✕', '한 달 만에 결과 기대하기', '변화는 바깥보다 안에서 먼저 일어납니다'), ('✕', '하루 무너지면 통째로 포기', '다음 날 이어가면 그대로 쌓입니다'), ('✕', '상대가 먼저 바뀌길 기다리기', '점프 버튼은 내 쪽에 있습니다')]),
        EN('Ways to kill the heat right before it boils: expecting results in a month, quitting after one bad day (just continue tomorrow), waiting for your partner to change first. The button is on your side.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '흔들릴 때 → 반응 vs 관찰'), ('2', '깨달음은 → 머릿속 vs 기록'), ('3', '같은 실수 → 반복 vs 원칙')]),
        '    <div class="rule"></div>',
        P('변화는 서서히,<br>점프는 한순간.', 'big'),
        P('지금 몇 도쯤 와 있는 것 같나요? 댓글로 숫자만 남겨주세요.', 'sub'),
        CTA('저장 → 또 흔들린 날 다시 보기', '5분 저널링으로 감정 정리하는 법'),
        EN('Check: when shaken, do you react or observe? Do insights stay in your head or get written down? Do mistakes repeat or become rules? Change is gradual. The jump happens in a moment.')])),
], caption='''불안형이든 회피형이든, 애착유형이 어느 날 한 번에 바뀌는 것처럼 보이는 순간에는 원리가 있습니다.

익숙한 패턴은 불편해도 '아는 길'로 느껴져서, 결심만으로는 사흘을 넘기기 어렵습니다.
나를 정확히 보기, 감정을 한 발 뒤에서 지켜보기, 배운 것을 내 기준으로 만들기.
이 세 단계가 조용히 쌓이면, 물이 100도에서 끓듯 반응이 통째로 달라집니다.
가장 실용적인 건 깨달음을 한 줄이라도 적어두는 것입니다.
단, 한 달 만에 결과를 재지 마세요. 하루 무너져도 다음 날 이어가면 됩니다.
다음 편은 "5분 저널링으로 감정 정리하는 법"입니다.
요즘 가장 자주 흔들리는 순간을 댓글이나 DM으로 남겨주세요.

Change looks sudden but builds quietly. See your patterns, watch feelings from one step back, and turn repeated lessons into personal rules. Write insights down. Like water at 100°C, reactions shift all at once.

관계를 이해하고 나를 지키기 위한 글입니다.

#애착유형 #안정형 #불안형 #연애심리 #자기성장''')

# ---------------- 20호 ----------------
EPS['20'] = dict(title='5분 저널링으로 감정 정리하는 법', next='뇌를 재구성하는 21일 프로젝트', slides=[
    slide(1, 'sil', '저널링', '\n'.join([
        H1('5분<br><em>감정</em><br>영수증'),
        P('오늘 마음이 어디에 얼마를 썼는지<br>다섯 줄로 적어보는 시간', 'sub'),
        EN('Five-minute journaling: an emotional receipt. A short daily note on where your heart spent its energy today, and how much.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('밤마다 머릿속이<br><em>시끄러워요</em>'),
        P('자려고 누우면<br>낮에 들은 한마디가<br>계속 재생돼요.<br>끄는 법이 있을까요?', 'quote'),
        P('머릿속에서 돌리면 무한 반복, 종이에 꺼내면 한 장으로 끝납니다.', 'sub'),
        EN('"When I lie down, one comment from today keeps replaying. Is there an off switch?" In your head it loops forever. On paper it ends on one page.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('아픈 건 사건보다<br>내가 붙인 <em>자막</em>'),
        P('"한 시간째 답이 없다"는 화면. "나한테 관심이 식었다"는 자막. 우리를 찌르는 건 대부분 자막 쪽입니다.'),
        P('적다 보면 사실과 해석 사이의 틈이 보입니다.', 'sub'),
        EN('What hurts is the subtitle, not the scene. "No reply for an hour" is the scene. "They\'re losing interest" is the subtitle you added. That\'s what stings. Writing reveals the gap.')])),
    slide(4, 'spot', '5줄 양식', '\n'.join([
        H2('영수증은<br><em>다섯 줄</em>이면 됩니다'),
        li([('1', '점수: 지금 감정의 세기 1~10'), ('2', '이름: 서운함, 억울함, 초조함'), ('3', '장면: 사실과 해석 나눠 쓰기'), ('4', '몸: 어디가 굳었는지'), ('5', '바람: 진짜 원했던 것')]),
        EN('Five lines is enough: score the feeling 1–10, name it precisely, split the scene into fact and interpretation, note where your body tensed, and write what you really wanted.')])),
    slide(5, 'glass', '점수', '\n'.join([
        H2('숫자를 붙이면<br>감정이 <em>작아집니다</em>'),
        P('"나 미치겠어" 대신 "초조함 6". 점수를 매기는 순간, 감정에 잠긴 사람에서 감정을 재는 사람이 됩니다.'),
        li([('·', '1~3 무시 가능'), ('·', '4~6 자꾸 떠오름'), ('·', '7~10 손에 아무것도 안 잡힘')]),
        EN('A number shrinks the feeling. Not "I\'m losing it" but "anxious, 6." Scoring moves you from drowning in a feeling to measuring it. 1–3 ignorable, 4–6 keeps coming back, 7–10 can\'t do anything else.')])),
    slide(6, 'lines', '장면과 몸', '\n'.join([
        H2('사실 한 줄,<br>해석 한 줄 <em>따로</em>'),
        STEPS([('사실', '저녁 약속 뒤 연락이 끊김'), ('해석', '"내가 지루했나 봐"'), ('확인', '다음 날: 휴대폰이 꺼져 있었음')]),
        P('몸도 함께 적으세요. 턱, 어깨, 명치. 생각이 말하기 전에 몸이 먼저 티를 냅니다.'),
        EN('Fact on one line, interpretation on another. Fact: no texts after dinner. Story: "I must have been boring." Next day: their phone had died. Note your body too; it alarms before your thoughts.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('마지막 줄이<br><em>진짜</em> 영수증입니다'),
        P('"주말 계획을 같이 짜고 싶었다"는 겉의 바람. 그 밑에는 "그 사람 일정에 내가 있고 싶다"가 있습니다. 찾으면 할 말이 달라집니다.'),
        li([('✕', '"또 혼자 다 정했네"'), ('○', '"나도 네 주말에 끼고 싶었어"')]),
        EN('The twist: the last line is the real receipt. "I wanted to plan the weekend together" sits on top of "I want a place in their life." Then your words change: not "You decided alone again" but "I wanted in."')])),
    slide(8, 'glass', '이어가기', '\n'.join([
        H2('잘 쓰는 날보다<br><em>쓰는 날</em>이 중요해요'),
        P('띄어쓰기가 틀려도, 세 단어여도 됩니다. 같은 시간, 같은 자리에서 5분. 그게 전부입니다.'),
        STEPS([('7장', '내 버튼이 보이기 시작함'), ('30장', '반복되는 장면이 보이기 시작함'), ('90장', '반응을 고르는 날이 늘기 시작함')]),
        EN('Showing up beats writing well. Typos and three-word entries are fine. Same time, same spot, five minutes. By entry 7, triggers start to show; by 30, patterns; by 90, more days you choose your response.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('이러면 일기가<br><em>재판</em>이 됩니다'),
        li([('✕', '상대 잘못만 길게 적기', '기록의 주인공은 나여야 합니다'), ('✕', '"나는 왜 이 모양이지"로 끝내기', '자책 말고 다음 선택으로 끝내기'), ('✕', '쓴 걸 상대에게 증거로 내밀기', '저널은 판결문이 아니라 거울입니다')]),
        EN('How a journal becomes a courtroom: listing only their faults (you\'re the main character), ending with "what\'s wrong with me" (end with a next choice), using it as evidence. It\'s a mirror, not a verdict.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '감정을 → 점수로 vs 덩어리로'), ('2', '장면을 → 사실 따로 vs 해석만'), ('3', '마지막 줄 → 바람 vs 원망')]),
        '    <div class="rule"></div>',
        P('머릿속은 무한 반복,<br>종이는 한 장.', 'big'),
        P('오늘 감정에 점수를 매긴다면 몇 점인가요? 댓글로 남겨주세요.', 'sub'),
        CTA('저장 → 잠 안 오는 밤 다시 보기', '뇌를 재구성하는 21일 프로젝트'),
        EN('Check: do you score feelings or leave them as a lump? Separate fact from interpretation? End with a need or a grudge? In your head it loops forever. On paper it\'s one page.')])),
], caption='''불안형 애착으로 밤마다 머릿속이 시끄럽다면, 가장 작은 도구는 하루 5분 감정 저널링입니다.

같은 장면에도 내가 붙이는 자막은 다릅니다. 적다 보면 장면과 자막 사이의 틈이 보입니다.
점수, 감정의 이름, 사실과 해석, 몸의 반응, 진짜 바람. 다섯 줄이면 충분합니다.
가장 중요한 건 마지막 줄입니다. 진짜 바람을 찾으면 상대에게 건네는 말이 달라집니다.
단, 상대 잘못만 적는 기록은 일기가 아니라 재판이 됩니다.
다음 편은 "뇌를 재구성하는 21일 프로젝트"입니다.
오늘 감정에 점수를 매긴다면 몇 점인지 댓글이나 DM으로 남겨주세요.

A five-line emotional receipt: score the feeling, name it, split fact from interpretation, notice your body, and find what you really wanted. That last line changes what you say next.

관계를 이해하고 나를 지키기 위한 글입니다.

#불안형 #애착유형 #감정정리 #저널링 #연애심리''')

# ---------------- 21호 ----------------
EPS['21'] = dict(title='뇌를 재구성하는 21일 프로젝트', next='ISFP는 회피형일까? MBTI와 애착', slides=[
    slide(1, 'sil', '프로젝트', '\n'.join([
        H1('뇌를<br>다시 짜는<br><em>21일</em>'),
        P('성격은 그대로여도<br>애착 습관은 바뀔 수 있습니다', 'sub'),
        EN('A 21-day project to rewire your brain. Your personality may stay the same, but attachment habits can change.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('사람은 안 변한다는 말,<br><em>정말</em>일까요'),
        P('연애할 때마다<br>같은 데서 무너져요.<br>원래 이렇게<br>생겨먹은 걸까요?', 'quote'),
        P('성격은 잘 안 바뀝니다. 그런데 애착은 바뀝니다. 둘은 다른 이야기입니다.', 'sub'),
        EN('"Every relationship, I fall apart at the same spot. Am I just built this way?" Personality rarely changes. Attachment patterns can. Those are two different stories.')])),
    slide(3, 'lines', '근거', '\n'.join([
        H2('같은 나인데<br>연애마다 <em>달랐다면</em>'),
        P('어떤 연애에선 집착했고, 어떤 연애에선 느긋했던 적 있지 않나요? 성격이 바뀐 게 아니라 애착 반응이 달라진 겁니다.'),
        P('움직인다는 건, 바꿀 수 있다는 뜻입니다.', 'sub'),
        EN('Same you, different relationships. Ever been clingy in one and relaxed in another? Your personality didn\'t change; your attachment response did. If it moves, it can change.')])),
    slide(4, 'spot', '원리', '\n'.join([
        H2('풀숲에 내는<br><em>첫 발자국</em>'),
        P('뇌의 반응도 풀밭의 길과 같습니다. 늘 걷던 불안의 길은 넓고, 새 길은 아직 풀숲입니다. 여러 번 걸어야 발자국이 보입니다.'),
        P('21일은 마법의 숫자가 아니라, 첫 발자국을 내기 좋은 길이입니다.', 'sub'),
        EN('A path forms where you walk often. Your old anxious route is wide; the new one is still tall grass. It takes repeated steps before footprints show. 21 days isn\'t magic, just a good length to start a trail.')])),
    slide(5, 'glass', '1주차', '\n'.join([
        H2('1주차,<br><em>알아차리기</em>'),
        P('바꾸려 하지 말고 잡아내기만 합니다. 흔들린 순간, 그때 떠오른 문장, 내가 한 행동.'),
        li([('·', '"또 나만 애쓰네"'), ('·', '"말하면 귀찮아하겠지"'), ('·', '"어차피 다 떠나"')]),
        EN('Week 1: notice. Don\'t change anything yet, just catch it: the shaky moment, the sentence that popped up, what you did. "I\'m the only one trying." "They\'ll find me annoying." "Everyone leaves anyway."')])),
    slide(6, 'lines', '2주차', '\n'.join([
        H2('2주차,<br>믿음 <em>뒤집어 보기</em>'),
        P('1주 동안 모은 문장에 반대 질문을 던집니다. 증거가 있는지, 다르게 볼 수는 없는지.'),
        li([('✕', '"먼저 연락하면 지는 거야"'), ('○', '"먼저 연락한 쪽이 더 여유 있는 걸지도"')]),
        EN('Week 2: flip the belief. Question the sentences you caught. Is there evidence? Another way to see it? "Texting first means losing" becomes "Maybe the one who texts first is the relaxed one?"')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('3주차,<br>안정형처럼 <em>움직이기</em>'),
        P('확신이 생길 때까지 기다리지 않습니다. "안정형이라면 지금 어떻게 할까?" 묻고, 그대로 한 번 해봅니다.'),
        P('행동이 먼저 바뀌면 믿음이 뒤따라옵니다. 사람은 스스로 기대하는 쪽으로 움직입니다.', 'sub'),
        EN('The twist, week 3: act secure before you feel secure. Ask "What would a secure person do right now?" and do it once. When behavior changes first, belief follows. People move toward what they expect of themselves.')])),
    slide(8, 'glass', '상황별', '\n'.join([
        H2('지금 혼자라면,<br>곁에 <em>누가</em> 있다면'),
        STEPS([('혼자', '주말 하루를 온전히 나와 보내기'), ('둘이', '내 기록 한 줄을 먼저 나눠 보기')]),
        P('상대가 있다면 같이 하자고 조르기보다, 내가 하는 걸 조용히 보여주는 쪽이 오래갑니다.'),
        EN('If you\'re alone: spend one full weekend day with yourself. If someone\'s beside you: share one line from your notes first. Quietly showing your effort lasts longer than pushing them to join.')])),
    slide(9, 'spot', '함정', '\n'.join([
        H2('21일이 지나도<br><em>제자리</em> 같다면'),
        li([('✕', '하루 빠졌다고 1일부터 다시', '빠진 날은 건너뛰고 이어가면 됩니다'), ('✕', '기분이 나아졌는지만 확인', '변화는 기분보다 행동에서 먼저 보입니다'), ('✕', '21일로 끝내기', '첫 길이 났을 뿐, 걸을수록 넓어집니다')]),
        EN('If day 21 feels like nothing changed: don\'t restart after one missed day, just continue. Check behavior, not only mood; it shifts first. And don\'t stop at 21. The trail widens as you keep walking.')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '흔들릴 때 → 잡아냄 vs 휩쓸림'), ('2', '옛 믿음 → 의심 vs 확신'), ('3', '다음 행동 → 새 길 vs 옛 길')]),
        '    <div class="rule"></div>',
        P('성격은 그대로,<br>길은 새로.', 'big'),
        P('21일 동안 가장 먼저 바꾸고 싶은 습관 하나, 댓글로 남겨주세요.', 'sub'),
        CTA('저장 → 오늘을 1일로 다시 보기', 'ISFP는 회피형일까? MBTI와 애착'),
        EN('Check: when shaken, do you catch it or get swept away? Do you doubt the old belief or trust it? Take the new path or the old one? Same personality, new path.')])),
], caption='''애착유형은 성격과 달리 바뀔 수 있습니다. 불안형도 회피형도 21일이면 첫 길은 낼 수 있습니다.

같은 사람도 어떤 연애에선 집착하고, 어떤 연애에선 느긋해집니다. 애착 반응은 움직입니다.
1주차는 알아차리기, 2주차는 믿음 뒤집어 보기, 3주차는 안정형처럼 움직여 보기.
행동이 먼저 바뀌면 믿음은 뒤따라옵니다.
단, 21일은 마법의 숫자가 아닙니다. 하루 빠져도 처음부터 다시 할 필요 없이 이어가면 됩니다.
다음 편은 "ISFP는 회피형일까? MBTI와 애착"입니다.
21일 동안 가장 먼저 바꾸고 싶은 습관을 댓글이나 DM으로 남겨주세요.

Personality rarely changes, but attachment habits can. Week 1: notice. Week 2: question old beliefs. Week 3: act secure before you feel it. 21 days isn't magic, just a good start for a new path.

관계를 이해하고 나를 지키기 위한 글입니다.

#애착유형 #안정형 #불안형 #자기계발 #연애심리''')

# ---------------- 22호 ----------------
EPS['22'] = dict(title='ISFP는 회피형일까? MBTI와 애착', next='설렘의 정체, 로맨스의 실체', slides=[
    slide(1, 'sil', 'MBTI', '\n'.join([
        H1('ISFP는<br><em>회피형</em><br>일까?'),
        P('MBTI와 애착유형을<br>같은 줄에 놓으면 생기는 오해', 'sub'),
        EN('Is every ISFP avoidant? What goes wrong when you line up MBTI types and attachment styles as if they were the same thing.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('ISFP랑 썸 중인데<br><em>회피형</em>이라던데요'),
        P('연락이 느리고<br>속마음을 잘 안 보여요.<br>ISFP는 원래 회피형이라는데<br>기다려도 될까요?', 'quote'),
        P('네 글자로는 그 사람의 연애 습관까지 읽을 수 없습니다.', 'sub'),
        EN('"They\'re slow to text and keep feelings hidden. People say ISFPs are avoidant. Should I wait?" Four letters can\'t tell you someone\'s relationship habits.')])),
    slide(3, 'lines', '핵심', '\n'.join([
        H2('둘은<br><em>재는 것</em>이 다릅니다'),
        P('MBTI는 내가 편하게 느끼는 방식을 보는 성향 검사, 애착은 겪어온 관계가 남긴 습관입니다. 같은 ISFP도 걸어온 관계에 따라 전혀 다릅니다.'),
        P('악기는 저마다 달라도, 연주하는 습관은 배운 것입니다.', 'sub'),
        EN('They measure different things. MBTI describes preferences; attachment is a habit left by relationships you lived through. Two ISFPs can be completely different. The instrument is one thing; how you play it is learned.')])),
    slide(4, 'spot', '오해', '\n'.join([
        H2('이런 공식은<br><em>버리세요</em>'),
        li([('✕', 'I는 회피형, E는 불안형'), ('✕', 'F는 집착, T는 무심'), ('✕', 'P는 잠수, J는 통제')]),
        P('조용한 사람이 연인에겐 누구보다 깊이 기대하고, 표현 많은 사람이 가까워지면 물러서기도 합니다.'),
        EN('Drop these formulas: introverts avoidant, extroverts anxious; feelers cling, thinkers don\'t care; perceivers ghost, judgers control. Quiet people can expect deeply; expressive ones can back away up close.')])),
    slide(5, 'glass', 'S와 N', '\n'.join([
        H2('흔들릴 때<br>S와 N의 <em>차이</em>'),
        STEPS([('S', '불확실한 내일이 불안 → 계획 확인'), ('N', '상상이 질주 → 답장 하나로 결말까지')]),
        P('안정되면 S는 작은 기념일까지 챙기고, N은 같이 해볼 새로운 걸 먼저 꺼냅니다.'),
        EN('When shaken, S and N wobble differently. S fears an uncertain tomorrow; N\'s imagination writes the ending from one late text. Secure, S remembers the small anniversaries and N suggests new things to try.')])),
    slide(6, 'lines', 'T와 F', '\n'.join([
        H2('차가운 T 속의 불안,<br>다정한 F 속의 <em>폭풍</em>'),
        P('말수 적은 T가 밤새 읽씹을 곱씹기도 하고, 늘 웃던 F가 한순간 문을 닫아버리기도 합니다.'),
        P('겉의 기질과 속의 애착은 따로 움직입니다.', 'sub'),
        EN('Anxiety under a cool T, a storm inside a gentle F. A quiet T may replay an unanswered text all night. An always-smiling F may suddenly shut the door. Temperament and attachment move separately.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('질문을 <em>바꾸면</em><br>길이 보입니다'),
        P('유형은 사람을 찍는 도장이 아니라, 지금 상태를 들여다보는 돋보기입니다.'),
        li([('✕', '"ISFP는 회피형이야?"'), ('○', '"이 ISFP는 지금 어떤 상태지?"'), ('○', '"요즘 내 불안은 어디서 올라오지?"')]),
        EN('The twist: change the question. Not "Are ISFPs avoidant?" but "What state is this ISFP in right now?" or "Where is my anxiety coming from lately?" Use type as a magnifier, not a stamp.')])),
    slide(8, 'glass', '안정되면', '\n'.join([
        H2('같은 유형도<br>안정되면 <em>이렇게</em>'),
        li([('J', '계획이 틀어져도 상대를 탓하지 않음'), ('P', '즉흥적이어도 약속 시간은 지킴'), ('T', '결론 전에 "힘들었겠다" 한마디'), ('F', '서운함은 하루 묵혔다 말함')]),
        EN('Same types, secure version: J doesn\'t blame a partner when plans fall apart; P is spontaneous but on time; T says "that must have been hard" before the solution; F lets hurt settle a day before talking.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('유형으로 사람을<br><em>미리</em> 거르지 마세요'),
        li([('✕', '"ISFP라서 안 될 거야"', '네 글자는 결과가 아니라 출발선입니다'), ('✕', '상대 행동을 전부 유형 탓으로', '같은 행동도 애착 상태가 원인일 수 있습니다'), ('✕', '내 불안을 "F라서"로 덮기', '기질 탓은 변화의 문을 닫습니다')]),
        EN('Don\'t filter people by type in advance: "They\'re ISFP, it won\'t work" (four letters are a starting line), blaming every behavior on type, or covering your own anxiety with "I\'m just an F."')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '유형을 → 판정용 vs 이해용'), ('2', '상대 행동 → 유형 탓 vs 상태 보기'), ('3', '내 불안 → 기질 탓 vs 바꿀 습관')]),
        '    <div class="rule"></div>',
        P('기질은 악기,<br>애착은 연주.', 'big'),
        P('내 MBTI와 애착유형 조합, 댓글로 알려주세요.', 'sub'),
        CTA('저장 → 유형 탓하고 싶을 때 다시 보기', '설렘의 정체, 로맨스의 실체'),
        EN('Check: do you use type to judge or to understand? Blame type or look at someone\'s current state? Treat your anxiety as fixed or as a habit you can change? Temperament is the instrument; attachment is how you play.')])),
], caption='''"ISFP는 원래 회피형"이라는 말, 믿어도 될까요? MBTI와 애착유형은 재는 것부터 다릅니다.

MBTI는 내가 편한 방식을 보는 성향 검사이고, 애착은 겪어온 관계가 남긴 습관입니다.
그래서 같은 ISFP도, 같은 T나 F도 애착은 전혀 다를 수 있습니다.
"ISFP는 회피형이야?" 대신 "이 사람은 지금 어떤 상태지?"라고 물어보면 길이 보입니다.
단, 유형으로 사람을 미리 거르거나 내 불안을 기질 탓으로 덮지는 마세요.
다음 편은 "설렘의 정체, 로맨스의 실체"입니다.
내 MBTI와 애착유형 조합을 댓글이나 DM으로 알려주세요.

MBTI describes preferences; attachment is a habit learned through relationships. No type is automatically avoidant or anxious. Ask what state a person is in, not what four letters they have.

관계를 이해하고 나를 지키기 위한 글입니다.

#회피형 #애착유형 #MBTI #ISFP #연애심리''')

# ---------------- 23호 ----------------
EPS['23'] = dict(title='설렘의 정체, 로맨스의 실체', next='혼란형 애착, 다가오다 밀어내는 이유', slides=[
    slide(1, 'sil', '실체', '\n'.join([
        H1('그 설렘,<br>정말<br><em>사랑</em><br>일까'),
        P('심장이 뛰는 이유가<br>늘 좋은 이유는 아닙니다', 'sub'),
        EN('Is that flutter really love? A racing heart doesn\'t always mean something good.')])),
    slide(2, 'cold', '어느 DM', '\n'.join([
        H2('올 듯 말 듯한 연락,<br>그게 <em>설렘</em>인 줄 알았어요'),
        P('어떤 날은 다정하고<br>어떤 날은 차가웠어요.<br>그 사람만 생각하다<br>제가 사라졌어요.', 'quote'),
        P('설렘과 불안은 심장 박동만 봐서는 구분이 안 됩니다.', 'sub'),
        EN('"Some days warm, some days cold. I thought about them so much I disappeared." From heartbeat alone, excitement and anxiety look exactly the same.')])),
    slide(3, 'lines', '되묻기', '\n'.join([
        H2('가끔 주는 관심이<br>더 <em>강하게</em> 묶습니다'),
        P('언제 터질지 모르는 슬롯머신이 손을 못 떼게 하듯, 예측할 수 없는 다정함은 뇌를 기다림에 붙잡아 둡니다.'),
        P('애틋함이라기보다, 보상을 기다리는 뇌의 반응에 가깝습니다.', 'sub'),
        EN('Occasional attention binds harder. Like a slot machine you can\'t walk away from, unpredictable affection keeps your brain hooked on waiting. It\'s not longing; it\'s a reward circuit.')])),
    slide(4, 'spot', '구분법', '\n'.join([
        H2('설렘인지 경보인지<br><em>몸</em>에게 물어보세요'),
        STEPS([('설렘', '만나고 나면 더 나다워짐'), ('경보', '만나고 나면 더 작아짐')]),
        P('두근거림 뒤에 남는 게 힘인지 피로인지 보세요. 같은 심장 소리라도 남기는 흔적이 다릅니다.'),
        EN('Excitement or alarm? Ask your body. Excitement: you feel more like yourself after seeing them. Alarm: you feel smaller. Notice whether a racing heart leaves energy or exhaustion behind.')])),
    slide(5, 'glass', '경보 신호', '\n'.join([
        H2('로맨스가 아니라<br><em>경보</em>일 때'),
        li([('·', '답장 시간이 하루 기분을 정함'), ('·', '그 사람 기분 따라 내 계획이 바뀜'), ('·', '싸운 뒤 사과는 늘 내 몫'), ('·', '친구 약속을 비워두고 기다림'), ('·', '가까워지면 오히려 도망치고 싶음')]),
        P('두 개 넘게 끄덕였다면, 사랑의 크기보다 애착의 모양을 볼 때입니다.', 'sub'),
        EN('Alarm, not romance: reply times set your mood, their mood rewrites your plans, you always apologize after fights, you keep your calendar empty for them, or closeness makes you want to run.')])),
    slide(6, 'lines', '실체', '\n'.join([
        H2('진짜 로맨스는<br>생각보다 <em>조용합니다</em>'),
        P('연락이 언제 올지 계산하지 않아도 되는 사이. 다정함이 날씨처럼 바뀌지 않는 사람. 처음엔 밋밋해 보일 수 있습니다.'),
        P('잔잔한 난로는 불꽃놀이보다 덜 화려하지만, 밤새 따뜻합니다.', 'sub'),
        EN('Real romance is quieter than you think. No calculating when they\'ll text; warmth that doesn\'t change like the weather. It can feel plain at first. A stove is less flashy than fireworks, but warm all night.')])),
    slide(7, 'hands', '반전', '\n'.join([
        H2('혼자 다 버티는 게<br><em>안정</em>은 아닙니다'),
        P('아무도 필요 없는 척은 또 다른 갑옷일 수 있습니다. 나를 세우는 힘과, 기댈 사람을 고르는 눈. 둘 다 있어야 합니다.'),
        li([('○', '혼자서도 하루가 무너지지 않음'), ('○', '힘들 땐 "도와줘"를 말할 수 있음')]),
        EN('The twist: enduring everything alone isn\'t security. Acting like you need no one can be armor. You need both: the strength to stand, and an eye for whom to lean on. Fine alone, and able to say "help me."')])),
    slide(8, 'glass', '다시 고르기', '\n'.join([
        H2('설렘의 기준을<br><em>다시</em> 세우기'),
        STEPS([('전', '애타게 하는 사람에게 끌림'), ('후', '편안하게 하는 사람에게 머묾')]),
        P('처음 몇 번은 편안함이 지루함처럼 느껴집니다. 그 어색함은 뇌가 새 기준에 적응하는 소리입니다.'),
        EN('Reset your standard for excitement. Before: drawn to people who keep you longing. After: staying with people who make you feel at ease. At first ease feels like boredom; that\'s your brain adjusting.')])),
    slide(9, 'spot', '절대 금지', '\n'.join([
        H2('이 말로<br><em>버티지</em> 마세요'),
        li([('✕', '"이 정도 아픔은 사랑이라서"', '사랑은 나를 지우는 대가를 요구하지 않습니다'), ('✕', '"다정한 날도 있으니까"', '가끔의 다정함이 가장 강한 미끼입니다'), ('✕', '"내가 더 잘하면 괜찮아질 거야"', '혼자 메우는 관계는 오래 못 갑니다')]),
        EN('Don\'t hold on with these lines: "This much pain means it\'s love" (love doesn\'t require erasing you), "They have sweet days too" (occasional sweetness is the strongest hook), "If I try harder it\'ll be fine."')])),
    slide(10, 'cold', '3초 진단', '\n'.join([
        li([('1', '만나고 나면 → 힘 vs 피로'), ('2', '다정함이 → 한결같음 vs 날씨'), ('3', '나의 일상 → 그대로 vs 사라짐')]),
        '    <div class="rule"></div>',
        P('두근거림보다<br>편안함을 믿을 것.', 'big'),
        P('지금의 설렘, 힘인가요 피로인가요? 댓글로 알려주세요.', 'sub'),
        CTA('저장 → 마음이 출렁이는 날 다시 보기', '혼란형 애착, 다가오다 밀어내는 이유'),
        EN('Check: do you leave with energy or fatigue? Is their warmth steady or weather-like? Does your daily life stay intact or vanish? Trust ease over a racing heart.')])),
], caption='''연락이 올 듯 말 듯해서 애타는 그 설렘, 사실은 불안형 애착이 울리는 경보일 수 있습니다.

예측할 수 없는 다정함은 슬롯머신처럼 뇌를 기다림에 붙잡아 둡니다.
구분법은 간단합니다. 만나고 나서 더 나다워지면 설렘, 더 작아지면 경보입니다.
진짜 로맨스는 생각보다 조용합니다. 처음엔 그 편안함이 지루하게 느껴질 수도 있습니다.
단, 혼자 다 버티는 게 안정은 아닙니다. 나를 세우는 힘과 기댈 사람을 고르는 눈이 함께 필요합니다.
다음 편은 "혼란형 애착, 다가오다 밀어내는 이유"입니다.
지금의 설렘이 힘인지 피로인지 댓글이나 DM으로 남겨주세요.

Unpredictable affection hooks the brain like a slot machine. If you feel more like yourself after seeing them, it's excitement; if you feel smaller, it's an alarm. Real romance is quieter than you think.

관계를 이해하고 나를 지키기 위한 글입니다.

#불안형 #애착유형 #설렘 #연애심리 #건강한연애''')

for n, ep in EPS.items():
    open(f'{here}/body_{n}.html', 'w').write(''.join(ep['slides']))
    open(f'{here}/caption_{n}.txt', 'w').write(ep['caption'].strip() + '\n')
    print(n, ep['title'])
import json
json.dump({n: {'title': e['title'], 'next': e['next']} for n, e in EPS.items()}, open(f'{here}/batch_19_23.json', 'w'), ensure_ascii=False)
