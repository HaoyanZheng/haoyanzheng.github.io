#!/usr/bin/env python3
import csv
import re
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 [
 {
            id: 1,
            topicCn: "P0｜万能开头结构｜所有题都能用",
            promptFr: "",
            promptCn: "",
            answerFr: `Je pense que c’est un sujet intéressant. En fait, je n’avais jamais vraiment réfléchi à ce thème avant. Je comprends que certaines personnes ont un avis positif parce que…
Premièrement, …
Deuxièmement, …
En même temps, je comprends aussi qu’il y ait d’autres personnes qui ont une opinion différente, parce que…
D’après moi, il faut adopter une approche équilibrée. Il est important de profiter des avantages, tout en évitant les risques potentiels.`,
            answerCn: `这是一个有趣/值得思考的话题，我以前没想过这方面的问题。
            我理解有的人支持这样的观点/认为xx是有利的因为：
            分论点1 （正向）+ 说理1 + 举例1
            分论点2 （正向）+ 说理2 + 举例2
            分论点3 （反向）+ (举例3)
            结论`
          },
          {
            id: 2,
            topicCn: "P1｜科技与生活｜网络/手机坏处：成瘾、视力、运动减少",
            promptFr: "Pour quelles raisons voudrait-on développer le tourisme dans un pays ?",
            promptCn: "第二段坏处",
            answerFr: `De plus, une utilisation excessive d’Internet peut entraîner une dépendance. Les réseaux sociaux et les vidéos courtes, par exemple, peuvent devenir très addictifs. Certaines personnes passent plusieurs heures par jour sur leur téléphone, ce qui nuit à leur santé, notamment à la vue et à l’activité physique. Il est donc important de trouver un bon équilibre entre le temps passé en ligne et les activités en plein air.`,
            answerCn: `其次，过度使用会导致依赖，短视频和社交媒体尤其容易上瘾，很多人每天花数小时刷手机，影响视力与运动量，因此要平衡线上时间与户外活动。`
          },
          {
            id: 3,
            topicCn: "P1｜科技与生活｜互联网类万能结论",
            promptFr: "Pour quelles raisons voudrait-on développer le tourisme dans un pays ?",
            promptCn: "总结",
            answerFr: `En conclusion, même si les avis sont partagés, je pense qu’Internet peut réellement améliorer notre vie, à condition de l’utiliser avec responsabilité, prudence et modération.`,
            answerCn: `总之，虽然看法不一，但我认为互联网在负责任、谨慎且适度使用的前提下，确实能改善我们的生活。`
          },
          {
            id: 4,
            topicCn: "P1｜国外生活/移民/语言融入｜国际职场",
            promptFr: "",
            promptCn: "第一段",
            answerFr: `Tout d’abord, vivre à l’étranger permet de développer une meilleure compréhension du monde du travail international. Dans un autre pays, les méthodes de management, l’organisation du travail et la communication professionnelle peuvent être très différentes. Cette expérience aide à mieux comprendre comment fonctionnent les entreprises dans d’autres contextes et à s’adapter à des environnements variés. Par exemple, une personne ayant travaillé à l’étranger peut plus facilement collaborer avec des équipes internationales ou s’intégrer dans une entreprise multinationale.`,
            answerCn: `首先，在国外生活能让人更好地理解国际化的职场环境。在另一个国家，管理方式、工作组织以及职场沟通可能都非常不同。这段经历能帮助人更好理解不同背景下企业如何运作，并学会适应多样的工作环境。例如，有海外工作经验的人，往往更容易与国际团队合作，或融入跨国公司。`
          },
          {
            id: 5,
            topicCn: "P1｜国外生活/移民/语言融入｜语言与沟通",
            promptFr: "",
            promptCn: "第二段",
            answerFr: `Ensuite, l’expérience à l’étranger renforce fortement les compétences en communication. Travailler ou vivre dans un autre pays oblige souvent à utiliser une langue étrangère et à communiquer avec des personnes issues de cultures différentes. Cela permet d’apprendre à s’exprimer plus clairement, à écouter les autres et à éviter les malentendus. Ces compétences sont très appréciées par les employeurs, notamment dans les secteurs liés au commerce international, à la technologie ou aux services.`,
            answerCn: `其次，海外经历能显著提升沟通能力。在国外工作或生活通常需要使用外语，并与来自不同文化的人交流。这会让人学会更清晰地表达、更好地倾听，并减少误解。这类能力很受雇主欢迎，尤其是在国际贸易、科技或服务等行业。`
          },
          {
            id: 6,
            topicCn: "P1｜国外生活/移民/语言融入｜适应能力与独立性",
            promptFr: "",
            promptCn: "第三段",
            answerFr: `De plus, vivre à l’étranger montre une capacité d’adaptation et d’autonomie, des qualités importantes pour réussir professionnellement. S’installer dans un nouveau pays demande de faire face à des situations inconnues, de résoudre des problèmes et de sortir de sa zone de confort. Cette expérience peut renforcer la confiance en soi et la capacité à gérer le stress, ce qui est un avantage dans de nombreux emplois à responsabilités.`,
            answerCn: `此外，在国外生活还能体现一个人的适应能力和独立性，而这些都是职业成功的重要素质。搬到一个新国家意味着要面对陌生情况、解决问题、走出舒适区。这种经历能增强自信，提高抗压能力，在许多需要承担责任的岗位上都是加分项。`
          },
          {
            id: 7,
            topicCn: "P1｜国外生活/移民/语言融入｜反方：国外经验不是必要条件",
            promptFr: "",
            promptCn: "第四段",
            answerFr: `Cependant, vivre à l’étranger n’est pas une condition indispensable pour réussir sa carrière. Si une personne souhaite travailler toute sa vie dans son pays d’origine, il peut être plus utile de bien connaître le marché local, les réseaux professionnels et les possibilités de promotion. Dans ce cas, l’expérience locale et les résultats concrets peuvent avoir plus de valeur que l’expérience internationale.`,
            answerCn: `不过，在国外生活并不是职业成功的必要条件。如果一个人计划一生都在本国发展，那么更了解本地市场、职业人脉以及晋升机会，可能更有用。在这种情况下，本地经验和可量化的成果，可能比国际经历更有价值。`
          },

          { type: "section", titleCn: "熟读", descFr: "", descCn: "" },
          {
            id: 8,
            topicCn: "P2｜公共交通/无车生活/环保｜减少私家车",
            promptFr: "",
            promptCn: "第一段",
            answerFr: `D’un côté, rendre les transports publics gratuits est un moyen efficace d’encourager les citoyens à réduire l’usage de la voiture individuelle. Lorsque les bus, métros ou tramways sont gratuits, de nombreuses personnes sont incitées à laisser leur voiture à la maison. Cela permet de diminuer le nombre de véhicules sur les routes, de réduire les embouteillages et de limiter les émissions de gaz à effet de serre. De plus, moins de voitures signifie aussi moins d’accidents de la route et moins de pollution sonore, ce qui améliore la qualité de vie en ville.`,
            answerCn: `一方面，让公共交通免费是一种有效方式，可以鼓励市民减少使用私人汽车。当公交车、地铁或有轨电车免费时，很多人会更愿意把车留在家里。这能减少道路上的车辆数量，缓解拥堵，并降低温室气体排放。此外，车更少也意味着交通事故更少、噪音污染更低，从而提升城市生活质量。`
          },
          {
            id: 9,
            topicCn: "P2｜公共交通/无车生活/环保｜反方：农村和城市过载",
            promptFr: "",
            promptCn: "第三段",
            answerFr: `Cependant, rendre les transports publics entièrement gratuits pose aussi des limites. Dans certaines régions rurales ou peu desservies, les transports publics ne sont pas suffisamment développés pour remplacer la voiture. De plus, dans les grandes villes, une gratuité totale pourrait entraîner une surcharge du réseau, avec des bus et des métros trop remplis, ce qui nuirait à la qualité du service. Il faut également tenir compte du coût financier pour les gouvernements, car l’entretien et le développement des infrastructures restent indispensables.`,
            answerCn: `不过，全面免费也有其局限。在一些农村或公共交通覆盖较少的地区，公共交通本身并不完善，难以替代私家车。此外，在大城市，如果完全免费，可能导致网络超负荷，出现公交和地铁过度拥挤，从而影响服务质量。还要考虑政府的财政负担，因为公共交通的维护与扩建仍然必不可少。`
          },
          {
            id: 10,
            topicCn: "P2｜公共交通/无车生活/环保｜折中方案",
            promptFr: "",
            promptCn: "第四段",
            answerFr: `C’est pourquoi une solution intermédiaire semble plus réaliste. Par exemple, la gratuité pourrait être réservée à certains groupes, comme les jeunes, les personnes âgées ou les ménages à faible revenu. Elle pourrait aussi s’appliquer uniquement à certaines périodes ou dans certaines zones urbaines. En parallèle, les gouvernements doivent continuer à investir dans des transports publics plus efficaces, propres et bien connectés.`,
            answerCn: `因此，一个折中的方案更现实。例如，免费政策可以优先面向某些群体，比如青少年、老年人或低收入家庭；也可以只在特定时段或特定城市区域实行。同时，政府还应持续投资建设更高效、更清洁、衔接更好的公共交通系统。`
          },
          {
            id: 11,
            topicCn: "P2｜单身/独居/家庭/孤独｜幸福不只取决于婚恋状态",
            promptFr: "",
            promptCn: "第一段",
            answerFr: `C’est une question assez délicate, car dans de nombreuses sociétés, le bonheur est souvent associé au couple, au mariage et à la famille. Pourtant, à mon avis, il est tout à fait possible de vivre heureux en étant célibataire. Le bonheur ne dépend pas uniquement du statut marital, mais plutôt de l’équilibre personnel, des choix de vie et de la qualité des relations, qu’elles soient amoureuses ou non.`,
            answerCn: `这是一个比较微妙的问题，因为在很多社会里，人们常常把幸福与恋爱、婚姻和家庭联系在一起。然而在我看来，一个人完全可以在单身状态下过得幸福。幸福并不只取决于婚恋状态，而更取决于个人的平衡、生活选择，以及各种关系的质量——不论是爱情关系还是非爱情关系。`
          },
          {
            id: 12,
            topicCn: "P2｜单身/独居/家庭/孤独｜自由与个人计划",
            promptFr: "",
            promptCn: "第二段",
            answerFr: `Tout d’abord, être célibataire offre une grande liberté dans l’organisation de la vie quotidienne. Une personne célibataire peut prendre ses décisions seule, gérer son temps libre comme elle le souhaite et poursuivre ses propres projets sans compromis constants. Par exemple, dans les grandes villes, il est facile de participer à des activités culturelles, à des événements sociaux ou sportifs, et de profiter de la vie urbaine de manière autonome. Cette liberté peut être une source importante de satisfaction personnelle.`,
            answerCn: `首先，单身能带来更大的生活自由。在日常生活的安排上，单身人士可以独立做决定，按自己的意愿管理时间，也能更专注于自己的计划，而不需要不断妥协。例如，在大城市里，人们很容易参加文化活动、社交或体育活动，并以更独立的方式享受城市生活。这种自由本身就可能成为重要的满足感来源。`
          },
          {
            id: 13,
            topicCn: "P2｜单身/独居/家庭/孤独｜反方：孤独与社交支持",
            promptFr: "",
            promptCn: "第五段",
            answerFr: `Cependant, il est vrai que le célibat peut aussi présenter des défis, comme le sentiment de solitude, surtout dans certaines périodes de la vie. C’est pourquoi il est essentiel pour une personne célibataire de maintenir une vie sociale active et de construire un réseau de soutien solide. Le bonheur en célibat demande donc un certain équilibre et une capacité à créer du sens dans sa vie.`,
            answerCn: `不过，单身也确实可能带来一些挑战，比如在某些人生阶段更容易感到孤独。因此，单身人士需要保持积极的社交生活，并建立可靠的支持网络。也就是说，单身的幸福需要一定的平衡能力，以及为生活创造意义的能力。`
          },
          {
            id: 14,
            topicCn: "P2｜父母权威/儿童教育/年轻人尊重｜规则与屏幕管理",
            promptFr: "",
            promptCn: "第二段",
            answerFr: `Ensuite, l’autorité joue un rôle essentiel dans l’apprentissage des règles et du respect, y compris dans le monde numérique. Dès le plus jeune âge, les enfants doivent comprendre qu’il existe des règles à la maison, à l’école et dans la société. Apprendre à respecter les horaires, les consignes des enseignants ou les règles de politesse aide l’enfant à mieux vivre avec les autres. Aujourd’hui, cela concerne aussi l’usage d’Internet et des écrans. Sans cadre, les enfants peuvent passer trop de temps en ligne ou être exposés à des contenus inadaptés. L’autorité permet donc d’encadrer ces usages et de préparer l’enfant à devenir un citoyen responsable.`,
            answerCn: `其次，权威在学习规则与尊重方面起着关键作用，包括在数字世界里也是如此。从很小的时候开始，孩子就需要明白：在家里、在学校以及在社会中都存在必须遵守的规则。学会遵守时间、遵守老师的要求、遵守礼貌规范，能帮助孩子更好地与他人相处。如今，这也涉及互联网和屏幕的使用。如果没有约束，孩子可能上网时间过长，或接触到不适合的内容。因此，父母的权威可以用来规范这些使用方式，并帮助孩子成长为负责任的公民。`
          },
          {
            id: 15,
            topicCn: "P2｜父母权威/儿童教育/年轻人尊重｜反方：不能过度权威",
            promptFr: "",
            promptCn: "第四段",
            answerFr: `Cependant, l’autorité ne doit jamais être excessive ni autoritaire. Une éducation fondée uniquement sur l’obéissance peut freiner la confiance en soi et empêcher l’enfant de développer son esprit critique. C’est pourquoi l’autorité doit toujours s’accompagner de dialogue et d’explications. Lorsque l’enfant comprend le sens des règles, il les accepte plus facilement et apprend à réfléchir par lui-même.`,
            answerCn: `不过，权威绝不能过度，也不能变成专制。只强调服从的教育方式，可能会阻碍孩子自信心的发展，并让他难以形成批判性思维。因此，权威必须始终伴随对话与解释。当孩子理解规则的意义时，他更容易接受，也会学会独立思考。`
          },
          ]

"""

# ---- Config ----
TACHE = 4                 # set 1/2/3/etc.
KIND  = "a"               # "a" for answers
OUT_CSV = Path("assets/tcfcaEO/t4.csv")
# ----------------

# Supports:
#   answerFr: ` ... `   (template strings; multiline)
#   answerFr: " ... "   (double quotes)
#   answerFr: ' ... '   (single quotes)
ANSWERFR_RE = re.compile(
    r"""
    \banswerFr\s*:\s*
    (?:                             # one of:
        `(?P<bt>[\s\S]*?)`          # 1) backticks (multiline)
      | "(?P<dq>(?:\\.|[^"\\])*)"   # 2) double quotes
      | '(?P<sq>(?:\\.|[^'\\])*)'   # 3) single quotes
    )
    \s*,?                           # optional trailing comma
    """,
    re.VERBOSE,
)

def extract_answerfr_strings(text: str) -> list[str]:
    answers: list[str] = []
    for m in ANSWERFR_RE.finditer(text):
        s = m.group("bt") or m.group("dq") or m.group("sq") or ""
        # Unescape for quoted strings (backticks usually already contain real newlines)
        s = (
            s.replace("\\r\\n", "\n")
             .replace("\\n", "\n")
             .replace("\\t", "\t")
             .replace('\\"', '"')
             .replace("\\'", "'")
             .replace("\\\\", "\\")
        ).strip()
        if s:
            answers.append(s)
    return answers

def main():
    answers = extract_answerfr_strings(RAW_JS)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tache", "kind", "idx", "text"])  # 4 columns
        for idx, sentence in enumerate(answers, start=1):
            w.writerow([TACHE, KIND, idx, sentence])

    print("Exported:", OUT_CSV)
    print("Count:", len(answers))

if __name__ == "__main__":
    main()
