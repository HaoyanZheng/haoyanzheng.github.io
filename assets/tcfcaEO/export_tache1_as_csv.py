#!/usr/bin/env python3
import csv
import re
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 [
 {
            id: 1, topicCn: "姓名",
            promptFr: "Comment vous appelez-vous ?",
            promptCn: "您叫什么名字？",
            answerFr: "Bonjour madame/ monsieur, je m’appelle Haoyan.",
            answerCn: "您好，我叫 Haoyan。"
          },
          {
            id: 2, topicCn: "年龄",
            promptFr: "Quel âge avez-vous ?",
            promptCn: "您多大了？",
            answerFr: "J’ai vingt et un ans.",
            answerCn: "我21岁。"
          },
          {
            id: 3, topicCn: "国籍",
            promptFr: "Quelle est votre nationalité ?",
            promptCn: "您的国籍是什么？",
            answerFr: "Je suis de nationalité chinoise. Actuellement, je suis étudiant international et je vis à Toronto avec mes amis.",
            answerCn: "我是中国国籍。目前我是一名国际学生，和朋友住在多伦多。"
          },
          {
            id: 4,
            topicCn: "性格",
            promptFr: "Comment êtes-vous ?",
            promptCn: "您的性格如何？",
            answerFr: "Je suis quelqu’un d’introverti, calme, et réfléchi. Mes amis me trouvent poli et généreux.",
            answerCn: "我比较内向、冷静、爱思考。朋友觉得我有礼貌而且大方。"
          },
          {
            id: 5,
            topicCn: "语言",
            promptFr: "Quelles langues parlez-vous ?",
            promptCn: "您会哪些语言？",
            answerFr: "Ma langue maternelle est le mandarin. Je parle couramment l’anglais et un peu de japonais. J’aime apprendre de nouvelles langues, parce que cela me permet de mieux comprendre d’autres cultures et de voir le monde sous un autre angle.",
            answerCn: "我的母语是普通话。我英语很流利，也会一点日语。我喜欢学新语言，因为这能帮助我理解其他文化，并从不同角度看世界。"
          },
          {
            id: 6,
            topicCn: "专业",
            promptFr: "Qu’est-ce que vous étudiez ?",
            promptCn: "您学什么专业？",
            answerFr: "J’étudie le génie robotique à l’université de Toronto et je suis actuellement en quatrième année. C’est un domaine difficile, mais je vois les grands changements que les robots apporteront à nos vies dans le futur. Je pense aussi qu’il y aura une forte demande sur le marché du travail et beaucoup de valeur à créer. C’est donc, à mon avis, un diplôme très prometteur.",
            answerCn: "我在多伦多大学学机器人工程，目前大四。这个领域很难，但我看到机器人未来会给生活带来巨大变化。我也认为就业市场需求会很大，价值空间也很高，所以我觉得这是很有前景的学位。"
          },
          {
            id: 7,
            topicCn: "实习经历",
            promptFr: "Avez-vous déjà fait des stages ?",
            promptCn: "您有实习经历吗？",
            answerFr: "Pendant mes études, j’ai eu l’occasion de faire plusieurs stages et travaux pratiques. L’an dernier, j’ai fait un stage au ministère des Transports de l’Ontario, où j’ai participé à l’inspection des autoroutes et j’ai suivi des travaux d’entretien. En parallèle, je travaille à l’Hôpital Général de Toronto, ce qui m’aide à développer mes compétences en communication et en organisation.",
            answerCn: "学习期间我做过多次实习和实践。去年我在安省交通厅实习，参与高速公路检查并跟进养护工作。同时我也在多伦多综合医院工作，帮助我提升沟通与组织能力。"
          },
          {
            id: 8,
            topicCn: "喜好",
            promptFr: "Quels sont vos centres d’intérêt ?",
            promptCn: "您的兴趣爱好是什么？",
            answerFr: "J’ai beaucoup de centres d’intérêt. J’aime le sport, surtout le badminton et la randonnée. J’aime aussi lire et j’écoute souvent les informations pour améliorer mon français. Ces activités m’aident à rester motivé et à garder un bon équilibre.",
            answerCn: "我兴趣很多。我喜欢运动，尤其是羽毛球和徒步。我也喜欢阅读，经常听新闻来提高法语。这些活动让我保持动力并维持平衡。"
          },
          {
            id: 9,
            topicCn: "家庭",
            promptFr: "Parlez-moi de votre famille.",
            promptCn: "请介绍一下您的家庭。",
            answerFr: "Mes parents sont commerçants en Chine et je suis enfant unique. Ça fait un an que je n’ai pas vu mes parents, mais on fait un appel vidéo chaque mois.",
            answerCn: "我父母在中国做生意，我是独生子女。我已经一年没见他们了，但我们每个月都会视频通话。"
          },
          {
            id: 10,
            topicCn: "未来计划",
            promptFr: "Quels sont vos projets pour l’avenir ?",
            promptCn: "您未来有什么计划？",
            answerFr: "Dans le futur, je souhaite continuer mes études et développer ma carrière au Canada. Je veux améliorer mon français et mon anglais pour m’intégrer facilement dans la société canadienne et réussir mes projets professionnels. Je suis motivé, curieux et prêt à relever de nouveaux défis.",
            answerCn: "未来我希望继续深造并在加拿大发展职业。我想提高法语和英语，更容易融入加拿大社会并实现职业目标。我很有动力、好奇，也准备迎接新挑战。"
          },
          {
            id: 11, topicCn: "难忘的事件",
            promptFr: "Racontez-moi un souvenir marquant.",
            promptCn: "请讲一个难忘的经历。",
            answerFr: "J’ai voyagé à Montréal l’année dernière, et cela m’a laissé un souvenir inoubliable. La ville a une ambiance différente grâce à sa culture francophone. J’ai beaucoup aimé la nourriture, le système de transport et l’architecture. Après l’obtention de mon diplôme, je prévois de m’y installer.",
            answerCn: "我去年去蒙特利尔旅行，留下了难忘回忆。这座城市因为法语文化氛围很不一样。我很喜欢那里的食物、交通系统和建筑。毕业后我计划搬去那里生活。"
          },
          {
            id: 12,
            topicCn: "城市",
            promptFr: "Où habitez-vous ?",
            promptCn: "您住在哪里？",
            answerFr: "J’habite à Toronto, une ville moderne connue pour ses gratte-ciels, sa diversité culturelle et sa vitalité économique.",
            answerCn: "我住在多伦多，这是一座现代化城市，以摩天大楼、多元文化和经济活力著称。"
          },
          {
            id: 13,
            topicCn: "住房条件",
            promptFr: "Comment est votre logement ?",
            promptCn: "您的住房情况如何？",
            answerFr: "Je loue une maison de quatre chambres avec des amis de l’université, située dans le quartier de Chinatown, juste en face de mon université. Le loyer est relativement abordable, ce qui est un avantage important pour moi. En revanche, le quartier est parfois bruyant et très fréquenté.",
            answerCn: "我和大学朋友合租了一套四居室的房子，位于唐人街，就在学校对面。房租相对比较实惠，这对我来说是一个重要的优点。不过，这个区域有时比较吵，人也很多。",
          },
          {
            id: 14,
            topicCn: "社区文化",
            promptFr: "Y a-t-il des événements dans votre quartier ?",
            promptCn: "您社区有哪些活动？",
            answerFr: "De temps en temps, il y a des événements culturels chinois dans mon quartier, surtout pendant les fêtes comme le Nouvel An chinois. Ces activités permettent aux habitants de se retrouver et de découvrir la culture. Cependant, comme je suis souvent occupé par mes études et mon travail, je participe rarement aux événements du quartier.",
            answerCn: "我的社区不时会举办一些华人文化活动，尤其是在春节等节日期间。这些活动让居民有机会聚在一起、了解文化。不过，由于我平时忙于学习和工作，很少参加社区活动。",
          },
          {
            id: 15,
            topicCn: "交通",
            promptFr: "Comment vous déplacez-vous ?",
            promptCn: "您平时怎么出行？",
            answerFr: "Comme je vis au centre-ville, il y a des tramways sur presque toutes les grandes rues. De plus, mon université est située près de plusieurs stations de métro, ce qui rend les déplacements très pratiques. En général, je peux facilement me déplacer dans le centre-ville sans avoir besoin de voiture.",
            answerCn: "因为我住在市中心，几乎每条主要街道都有有轨电车。此外，我的学校靠近多条地铁站，这让出行非常方便。总体来说，在市中心我不用开车也能很轻松地出行。",
          },
          {
            id: 16,
            topicCn: "气候",
            promptFr: "Quelle est votre saison préférée ?",
            promptCn: "你最喜欢的季节是什么？",
            answerFr: "L’été est ma saison préférée à Toronto, car le climat est agréable et confortable. Pendant les journées les plus chaudes, je reste généralement au travail ou à la maison, et je préfère sortir marcher ou faire de la randonnée le matin ou en soirée, quand la température est plus douce. Il y a souvent un peu de vent, ce qui rend l’ambiance encore plus agréable.",
            answerCn: "在多伦多，夏天是我最喜欢的季节，因为气候比较舒适。天气最热的时候，我通常在工作或在家，早上或傍晚气温较低时会出去散步或徒步。通常还会有一点风，让整体感觉更加舒服。",
          },
          {
            id: 17,
            topicCn: "气候",
            promptFr: "Quelle est la saison que vous aimez le moins ?",
            promptCn: "你最讨厌的季节是什么？",
            answerFr: "L’hiver est la saison que j’aime le moins à Toronto, car il est rude et glacial, ce qui rend la vie quotidienne plus difficile. Je dois porter un bonnet, des gants et un manteau d’hiver pour rester au chaud, surtout lorsque les températures sont très basses. Malgré cela, les déplacements restent souvent compliqués à cause du vent et de la neige présents chaque année.",
            answerCn: "在多伦多，冬天是我最不喜欢的季节，因为天气又冷又严酷，这让日常生活变得更加困难。为了保暖，我必须戴帽子、手套并穿上厚重的冬衣，尤其是在气温很低的时候。尽管如此，由于每年都会有大风和积雪，出行仍然经常不太方便。",
          },
          {
            id: 18,
            topicCn: "友谊关系",
            promptFr: "Parlez-moi de vos amis.",
            promptCn: "说说你的朋友。",
            answerFr: "J’ai beaucoup d’amis de l’université avec qui je reste en contact tout au long de l’année. Nous échangeons régulièrement des nouvelles et nous discutons aussi de nos difficultés, comme la recherche d’emploi, les candidatures aux études supérieures ou des questions liées à la vie quotidienne. C’est pour moi une excellente façon de rester informé et de suivre l’actualité en technologie, en politique et en économie.",
            answerCn: "我有很多大学朋友，我们全年都保持联系。我们经常互相分享近况，也会讨论一些困难，比如找工作、申请研究生，或者日常生活中的问题。对我来说，这也是了解科技、政治和经济动态的一种很好方式。",
          },
          {
            id: 19,
            topicCn: "个人物品",
            promptFr: "Quels objets sont importants pour vous ?",
            promptCn: "哪些物品对你很重要？",
            answerFr: "Comme je suis étudiant international au Canada, je ne possède pas de gros meubles ni d’objets de grande valeur. Je garde seulement l’essentiel, c’est-à-dire des affaires utiles et peu coûteuses, afin de pouvoir déménager facilement pour mes études ou pour le travail. Pour moi, les objets les plus importants sont mes outils de communication et de travail, notamment mon téléphone et mon iPad.",
            answerCn: "由于我是加拿大的国际学生，我没有大件家具或贵重物品。我只保留一些必需、实用而且不贵的东西，这样可以方便我因为学习或工作在加拿大搬家。对我来说，最重要的物品是沟通和学习用的工具，比如手机和 iPad。",
          },
          {
            id: 20,
            topicCn: "最想去的地方",
            promptFr: "Quel pays aimeriez-vous visiter ?",
            promptCn: "你最想去哪里？",
            answerFr: "Le pays que j’aimerais le plus visiter est l’Islande. Je privilégie un mode de vie calme et un bon équilibre entre la vie professionnelle et la vie personnelle, et l’Islande correspond bien à ces valeurs grâce à sa nature préservée. De plus, le climat hivernal y est généralement plus doux qu’à Toronto et le pays dispose d’un système de protection sociale fiable.",
            answerCn: "我最想去的国家是冰岛。我比较看重安静的生活方式以及工作与生活的平衡，而冰岛凭借其原始的自然环境很好地符合这些价值观。此外，那里的冬季气候通常比多伦多温和，而且社会保障体系也比较完善。",
          },
          {
            id: 21,
            topicCn: "为什么加拿大",
            promptFr: "Pourquoi voulez-vous vivre au Canada ?",
            promptCn: "你为什么想在加拿大生活？",
            answerFr: "Je pense que l’inclusivité, la protection de l’environnement et la qualité de vie sont les principales raisons pour lesquelles je souhaite vivre au Canada. Le pays offre une nature exceptionnelle, et comme j’aime beaucoup la nature, j’apprécie passer du temps près de l’océan, en montagne et observer les animaux. Enfin, le Canada est un pays multiculturel où différentes cultures et valeurs sont généralement respectées et bien accueillies.",
            answerCn: "我认为包容性、环境保护以及生活质量是我想在加拿大生活的主要原因。加拿大拥有非常出色的自然环境，而我本身很喜欢大自然，喜欢去海边、山区以及观察动物。最后，加拿大是一个多元文化国家，不同的文化和价值观通常都会受到尊重和欢迎。",
          }
          ]

"""

# ---- Config ----
TACHE = 1                 # set 1/2/3/etc.
KIND  = "a"               # "a" for answers
OUT_CSV = Path("assets/tcfcaEO/t1.csv")
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
