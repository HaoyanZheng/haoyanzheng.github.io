#!/usr/bin/env python3
import csv
import re
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 [
  {
            id: 1,
            topicCn: "文化传播",
            promptFr: "",
            promptCn: "第一段",
            answerFr: `Le voyage, les aliments, les films, les livres, la musique, les musées, l’art et les langues sont tous des moyens de transmettre et de partager la culture. En regardant des films, par exemple, nous pouvons découvrir facilement des cultures différentes. Cela nous aide à mieux comprendre le monde et à avoir une vision plus complète de la réalité qui nous entoure.`,
            answerCn: `旅行(国外学习/工作)，美食，电影，书籍，音乐，博物馆，艺术和语言都是文化传承和文化传播的手段。通过看电影，我们可以轻松的了解不一样的文化，这有利于我们更全面的认识和了解这个世界。`
          },
          {
            id: 2,
            topicCn: "文化传播",
            promptFr: "",
            promptCn: "第二段",
            answerFr: `Quand nous avons une meilleure compréhension du monde, surtout quand nous parlons plus de langues, cela nous aide beaucoup pour trouver un travail. Dans un monde où les cultures sont très liées aujourd’hui, parler plusieurs langues veut dire que nous avons la capacité de communiquer et de collaborer avec des personnes d’autres pays. Cette compétence nous donne un grand avantage dans la compétition professionnelle.`,
            answerCn: `当我们对于这个世界有更好的认识以后，尤其是当我们会说更多的语言，这对于我们找工作来说会有非常大的帮助。因为在如今这个文化高度融合的世界中，会说多门语言意味着我们有与别的国家的人沟通以及合作的能力，这个能力在职场的竞争中会给我们带来很大的优势。`
          },
          {
            id: 3,
            topicCn: "文化传播",
            promptFr: "",
            promptCn: "第三段",
            answerFr: `À l’école, au travail ou sur Internet, les jeunes peuvent facilement se faire des amis étrangers. Par exemple, ils aiment utiliser les réseaux pendant leur temps libre pour discuter et se divertir. En jouant en ligne ou en parlant avec des personnes sur les plateformes sociales, il devient facile d’échanger avec des amis d’autres pays et d’apprendre une nouvelle langue ou une nouvelle culture. Cela nous aide aussi à nous intégrer plus rapidement dans la vie locale.`,
            answerCn: `在学校，办公室以及网络空间，年轻人都很容易交到外国朋友。比如说年轻人喜欢在闲暇时间使用网络来社交和娱乐，在玩游戏或者与网友聊天的过程中，我们很容易与别国的朋友交流，学习到新的语言以及文化。这有利于我们更快的融入当地的生活。`
          },
          {
            id: 4,
            topicCn: "文化传播",
            promptFr: "",
            promptCn: "例子：语言好--更容易找到工作/找到更好的工作",
            answerFr: `Avant, quand je cherchais mon premier travail, je parlais seulement anglais. Je cherchais pendant 6 mois pour trouver un poste/ un emploi qui n’offre que 18 dollars par heure. Après avoir travaillé pendant un an, cette entreprise a fermé. J’ai donc perdu mon travail. Heureusement, l’année dernière, je suivais un cours de français après mon travail, avec cette nouvelle compétence, j’ai trouvé assez rapidement un autre travail. En plus, ce nouveau poste m’offre 30 dollars par heure. En même temps, mes collègues qui ne parlent pas d’anglais restent toujours au chômage.`,
            answerCn: `以前，当我找第一份工作的时候，我只会说英语。我找了六个月，才找到一份每小时只有18美元的工作。工作一年后，这家公司倒闭了，所以我失去了工作。幸运的是，去年我下班后上法语课。凭借这项新能力，我很快找到了另一份工作。而且，这份新工作每小时给我30美元。与此同时，我那些不会说英语的同事仍然处于失业状态。`
          },

          { type: "section", titleCn: "身心健康", descFr: "", descCn: "" },
          {
            id: 5,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "核心段语料：总起",
            answerFr: `Pour garder une bonne santé, nous devons généralement faire attention à deux aspects : d’une part l’activité physique, et d’autre part l’alimentation.`,
            answerCn: `为了保证身体健康，我们通常需要注意两个方面，一个是运动，一个是饮食。`
          },
          {
            id: 6,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "饮食风险",
            answerFr: `Tout d’abord, de la côté alimentation :

Les experts disent souvent que ‘on est ce qu'on mange’. Si nous consommons régulièrement des aliments trop sucrés, gras ou salés, nous risquons des maladies cardiaques, de l'obésité, voire du diabète.`,
            answerCn: `首先，从饮食方面来看：

专家们常说“人如其食”（我们吃什么，就成为什么）。如果我们经常摄入过多的糖分、脂肪或盐分，就有可能患上心脏病、肥胖，甚至糖尿病。`
          },
          {
            id: 7,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "营养建议",
            answerFr: `Si nous suivons les conseils des nutritionnistes – comme manger chaque jour deux portions de viande, cinq de fruits et légumes et deux produits laitiers – notre corps devient plus léger et énergique.`,
            answerCn: `如果我们遵循营养师的建议——例如每天摄入两份肉类、五份水果和蔬菜，以及两份乳制品——我们的身体会变得更轻松、更有活力。`
          },
          {
            id: 8,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "体育活动方面",
            answerFr: `Et puis de la côté activité physique :

Aujourd'hui, les jeunes restent souvent assis longtemps, se couchent tard et abusent des écrans, ce qui augmente fortement les problèmes de vue et de dos. xx provoquent des maladies à la tête…`,
            answerCn: `接下来是关于体育活动方面：

如今，年轻人经常长时间坐着，睡得很晚，并且过度使用电子屏幕，这大大增加了视力和背部出现问题的风险。`
          },
          {
            id: 9,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "不良习惯",
            answerFr: `Nous aimons aussi faire la fête tard, boire ou fumer : toutes ces habitudes nuisent à la santé.`,
            answerCn: `我们也喜欢熬夜参加派对、喝酒或抽烟：这些习惯都会损害健康。`
          },
          {
            id: 10,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "运动不足",
            answerFr: `De l’autre côté, étudier/ travailler/ jouer pendant trop longtemps réduit notre temps pour faire de l’exercice : la plupart d'entre nous ne font pas de sport régulièrement, ce qui empêche de garder un corps jeune et en forme.`,
            answerCn: `另一方面，学习/工作/游戏太长时间会减少我们锻炼的时间：我们大多数人都不经常锻炼，这使我们无法保持年轻和良好的体型。`
          },
          {
            id: 11,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "身体不好影响工作学习生活",
            answerFr: `Quand nous ne nous sentons pas bien, notre travail, nos études et notre vie quotidienne sont aussi touchés négativement. Cela peut également nous apporter un stress mental plus important.`,
            answerCn: `当我们身体不舒服的时候，我们的工作，学习和日常生活也会受到负面影响。我们也会因此承受更大的心理压力。`
          },
          {
            id: 12,
            topicCn: "身心健康",
            promptFr: "",
            promptCn: "心理健康比喻",
            answerFr: `Une personne est comme un téléphone portable et la santé mentale est comme sa mémoire. Bien que la mauvaise humeur et la pression ne soient pas visibles, elles occupent la mémoire. Il doit être nettoyé de temps en temps. Sinon, le téléphone va bientôt subir le dommage.`,
            answerCn: `一个人就像一部手机，而心理健康就像手机的内存。虽然坏情绪和压力看不见，但它们会占据内存，因此需要不时地清理。否则，这部“手机”很快就会受到损害。`
          },

          { type: "section", titleCn: "经济形势与金钱", descFr: "", descCn: "" },
          {
            id: 13,
            topicCn: "经济形势与金钱",
            promptFr: "",
            promptCn: "核心段语料：经济压力",
            answerFr: `La situation s'est aggravée avec la pandémie: l'économie mondiale a reculé, et toutes les entreprises, grandes ou petites, ont souffert. Pour les gens ordinaires comme nous, la hausse des prix partout et les risques de chômage rendent la vie très difficile.`,
            answerCn: `疫情使情况变得更加严重：全球经济倒退，无论大小企业都受到了影响。对于像我们这样的普通人来说，到处上涨的物价以及失业风险让生活变得非常困难。`
          },
          {
            id: 14,
            topicCn: "经济形势与金钱",
            promptFr: "",
            promptCn: "物价上涨例子",
            answerFr: `Prenons un exemple concret: Nos courses alimentaires coûtaient environ 300$ par semaine en 2019. Aujourd'hui, il faut au moins 600$ pour la même quantité... et la qualité n'est pas meilleure! Malheureusement, nos salaires n'ont pas doublé comme les prix.`,
            answerCn: `让我们举一个具体的例子：2019 年，我们一周的食品杂货大约花 300 加元。如今，购买同样的数量，至少要 600 加元……而且质量并没有更好！不幸的是，我们的工资并没有像物价一样翻倍。`
          },
          {
            id: 15,
            topicCn: "经济形势与金钱",
            promptFr: "",
            promptCn: "年轻人就业压力",
            answerFr: `Certains jeunes diplômés (comme moi) ne trouvent aucun emploi stable et doivent accepter des petits boulots en supermarché ou restaurant pour payer leur loyer. D'autres, des travailleurs expérimentés, voient leur entreprise fermer. Ils sont au chômage ou risquent d'être au chômage, obligés de prendre des postes moins payés qu'avant.`,
            answerCn: `一些刚毕业的年轻人（像我一样）找不到稳定的工作，只能接受在超市或餐馆等地方的短期工作来支付房租。另一部分有经验的员工则看到自己的公司倒闭。他们已经失业或面临失业，不得不接受比以前薪水更低的职位。`
          },
          {
            id: 16,
            topicCn: "经济形势与金钱",
            promptFr: "",
            promptCn: "有钱的好处/有时间的好处",
            answerFr: `Quand on a assez d'argent/de temps, on peut faire beaucoup plus de choses. Par exemple:

On peut emmener notre famille voyager à l'étranger: on découvre de nouvelles spécialités culinaires, on se détend, on passe du temps ensemble, on crée des mémoires importants et on peut même apprendre la culture et la langue locale.

Ou s'inscrire à des cours utiles ou passionnants: ça rend la vie plus intéressante, permet d'apprendre de nouvelles compétences et de se faire des amis. Peut-être qu'avec ces nouvelles connaissances, on pourra même trouver un meilleur travail!`,
            answerCn: `当我们有足够的钱 / 时间时，我们可以做更多的事情。例如：

我们可以带家人出国旅行：可以发现新的美食、放松身心、一起共度时光、创造美好的回忆，甚至还能学习当地的文化和语言。

或者报名参加一些有用或令人感兴趣的课程：这会让生活更有趣，也可以学到新的技能，结交朋友。也许凭借这些新知识，我们甚至能找到一份更好的工作！`
          },
          {
            id: 17,
            topicCn: "经济形势与金钱",
            promptFr: "",
            promptCn: "缺钱的后果",
            answerFr: `Par contre, si on manque d'argent :
On doit dire adieu aux loisirs. On ne peut même pas s'offrir un vrai bon repas. On stresse pour le loyer du mois suivant. C'est vraiment loin d'être la vie idéale!`,
            answerCn: `另一方面，如果我们缺钱：

我们只能告别娱乐活动，甚至连一顿真正好的饭都负担不起。我们还要为下个月的房租而焦虑。这真的离理想的生活太远了！`
          },

          { type: "section", titleCn: "科技与生活", descFr: "", descCn: "" },
          {
            id: 18,
            topicCn: "科技与生活",
            promptFr: "",
            promptCn: "核心段语料：第一段",
            answerFr: `Aujourd’hui, le développement d’Internet, des téléphones portables, des ordinateurs et des tablettes apporte beaucoup de commodité à notre vie quotidienne. Grâce à ces technologies, nous pouvons travailler à distance et suivre des cours en ligne, ce qui est très pratique.`,
            answerCn: `互联网，手机，电脑，平板电脑等科技的流行给我们的生活带来了不少便利。比如我们可以远程工作，可以远程上课。`
          },
          {
            id: 19,
            topicCn: "科技与生活",
            promptFr: "",
            promptCn: "核心段语料：第二段",
            answerFr: `Ces outils permettent aussi de gagner beaucoup de temps. Par exemple, nous pouvons commander des repas avec notre téléphone, sans avoir besoin de conduire jusqu’au restaurant ni de faire la queue. De plus, quelquefois, commander des repas sur certaines applications fait économiser de l’argent. +举例子`,
            answerCn: `这些科技的应用也会帮我们节省很多时间，比如我们可以用手机点外卖，省去开车到餐厅点餐和排队等待的时间。另外，在一些app上面点餐还可以省钱。`
          },
          {
            id: 20,
            topicCn: "科技与生活",
            promptFr: "",
            promptCn: "核心段语料：第三段",
            answerFr: `De plus, Internet et les nouvelles technologies rapprochent les personnes entre elles. En ce qui me concerne, je peux envoyer des messages à mes proches qui vivent à l’étranger ou faire des appels vidéo en temps réel. Autrefois, avant l’apparition de ces technologies, il fallait écrire des lettres ou passer des appels téléphoniques, ce qui était à la fois lent et coûteux. Aujourd’hui, grâce au téléphone portable et à Internet, tout est devenu beaucoup plus simple et plus rapide.`,
            answerCn: `网络和科技还可以拉进人与人之间的距离，尤其是对于我来说，我可以给国外的亲友发消息或者进行实时的视频通话，对比以前没有科技的时候，我们必须要通过写信或者电话来联系，又慢又昂贵。现在有了手机和网络，一切都变得更方便了。`
          },

          { type: "section", titleCn: "环保", descFr: "", descCn: "" },
          {
            id: 21,
            topicCn: "环保",
            promptFr: "",
            promptCn: "核心段语料：第一段",
            answerFr: `L'environnement est confronté à de nombreux problèmes environnementaux. Par conséquent, le développement durable et le bien-être de l'humanité sont également menacés. Il est donc fondamental que nous fassions tout ce qui est en notre pouvoir, même si c'est minime, pour contribuer à créer un environnement plus durable.`,
            answerCn: `环境正面临诸多环境问题。因此，人类的可持续发展和福祉也受到了威胁。

因此，我们必须尽自己所能去采取行动，即使是微不足道的努力，也有助于建设一个更加可持续的环境。`
          },
          {
            id: 22,
            topicCn: "环保",
            promptFr: "",
            promptCn: "核心段语料：第二段",
            answerFr: `Ces dernières années, de plus en plus de gens ont commencé à réaliser la gravité de l’impact négatif des activités humaines sur l’environnement. Par exemple, à cause de l’effet de serre, l’habitat des animaux diminue rapidement, menaçant leur survie. La réduction de la diversité des espèces menace également la survie humaine.`,
            answerCn: `近年来，越来越多的人开始意识到人类活动对环境造成的负面影响有多么严重。

例如，由于温室效应，动物的栖息地迅速减少，威胁到它们的生存。

物种多样性的减少同样也对人类的生存构成了威胁。`
          },
          {
            id: 23,
            topicCn: "环保",
            promptFr: "",
            promptCn: "核心段语料：塑料吸管例子",
            answerFr: `Par exemple, les pailles en plastique, qui sont souvent trop petites pour être recyclées correctement, finissent dans la nature et contribuent à la pollution de l’eau et des sols. Elles peuvent blesser les animaux marins qui les confondent avec de la nourriture. Si chacun de nous fait l'effort de refuser ou de remplacer les pailles en plastique par des alternatives réutilisables, comme celles en métal ou en bambou, nous pourrons réduire la quantité de déchets plastiques dans l’environnement.`,
            answerCn: `例如，塑料吸管通常太小，无法被正确回收，最后流入自然环境中，污染水源和土壤。它们可能会伤害到误食它们的海洋动物。如果我们每个人都努力拒绝使用或改用可重复使用的吸管，比如金属或竹制吸管，就可以减少环境中塑料垃圾的数量。`
          },
          {
            id: 24,
            topicCn: "环保",
            promptFr: "",
            promptCn: "核心段语料：个人行动",
            answerFr: `Même si les actions individuelles peuvent sembler insignifiantes, leur effet cumulé peut être très important. Quand des millions de personnes changent une petite habitude, cela peut faire une grande différence. Il est donc essentiel de commencer par soi-même, dans la vie quotidienne : dire non aux objets à usage unique, trier ses déchets, ou encore sensibiliser ses proches. Chaque petit geste compte pour protéger notre planète.`,
            answerCn: `虽然个人的行动看起来微不足道，但累积起来的影响可能非常大。当数百万人改变一个小习惯时，往往能带来巨大的变化。因此，从自己做起非常重要。在日常生活中，我们可以拒绝一次性用品、分类垃圾，或者向身边人宣传环保意识。每一个小小的举动，都是在为保护地球出一份力`
          }
          ]

"""

# ---- Config ----
TACHE = 3                 # set 1/2/3/etc.
KIND  = "a"               # "a" for answers
OUT_CSV = Path("assets/tcfcaEO/t3.csv")
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
