#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
[
          { type: "section", titleCn: "投诉信", descFr: "", descCn: "" },
          {
            id: 1, topicCn: "11-09旅行投诉",
            promptFr: "Rédigez une lettre de réclamation pour exprimer votre insatisfaction à l'égard des services fournis par une agence de voyage suite à une organisation défaillante de votre séjour. ",
            promptCn: "撰写一封投诉信，针对旅行社因行程组织不力/安排失当而导致你的旅程出现问题，表达你对其所提供服务的不满。",
            answerFr: `À l’attention du service client,
Je vous contacte suite aux problèmes rencontrés lors de mon dernier séjour organisé par votre agence de voyage du 7 au 10 mars.
Je suis profondément déçu par la situation rencontrée, notamment en ce qui concerne les aspects suivants :
Premièrement, l’hôtel réservé ne correspondait pas à la description. La piscine annoncée était en travaux et les chambres manquaient de propreté, ce qui a affecté mon séjour.
Deuxièmement, le guide est arrivé avec au moins 30 minutes de retard. Malgré ce retard, il a exigé le paiement d’une heure complète de service et a également réclamé un pourboire d’un montant excessif. Ce comportement me paraît inacceptable.
Compte tenu de ces désagréments, je vous demande un remboursement partiel des frais engagés.
Dans l’attente de votre réponse, je vous prie d’agréer, Madame, Monsieur, l’expression de mes salutations distinguées.
Haoyan`,
            answerCn: `致客户服务部：
我联系您，是因为在贵旅行社为我安排的 3 月 7 日至 3 月 10 日的最近一次行程中遇到了问题。
我对所遭遇的情况感到非常失望，尤其体现在以下方面：
首先，预订的酒店与描述不符。宣传中提到的游泳池正在施工，且房间卫生状况欠佳，这影响了我的住宿体验。
其次，导游迟到至少 30 分钟。尽管如此，他仍要求按完整一小时的服务收费，并且还索要金额过高的小费。我认为这种行为不可接受。
鉴于上述不便与困扰，我要求对已支付费用进行部分退款。
期待您的回复。此致敬礼（谨致崇高的敬意）。
Haoyan`
          },
          { type: "section", titleCn: "介绍名人", descFr: "", descCn: "" },
          {
            id: 2, topicCn: "9-04（Tâche 2）描述名人+名人对自己的影响（艺术家）",
            promptFr: "Vous rédigez un article de blog pour montrer votre admiration envers une personne célèbre ou non. Vous décrivez ses actions et expliquez pourquoi elle vous inspire.",
            promptCn: "你要写一篇博客文章，表达你对某个人（可以是名人，也可以不是名人）的敬佩。你需要描述他/她做过的事情，并解释为什么他/她能激励你。",
            answerFr: `Bonjour à tous,
Pour le concours « Mon artiste préféré », je voudrais vous parler d’Omar Sy, acteur français que j’admire énormément. 
Dans le film Intouchables, il incarne Driss, un jeune homme sans emploi qui devient l’aide à domicile de Philippe, un aristocrate devenu tétraplégique. Entre eux naît une amitié inattendue : humour, confiance et respect transforment leur quotidien et montrent que la dignité n’a pas de classe sociale. 
Omar Sy me touche par son énergie positive et son jeu naturel : il fait rire sans mépriser personne et il donne du courage face aux difficultés. Son parcours prouve qu’on peut réussir en restant simple. 
Et vous, quel artiste vous inspire ?`,
            answerCn: `大家好：
在“我最喜欢的艺术家”比赛中，我想向大家介绍一位我非常敬佩的法国演员——奥马尔·希（Omar Sy）。在电影《触不可及》（Intouchables）中，他饰演德里斯（Driss）：一个失业的年轻人，后来成为菲利普（Philippe）的居家护理助手。菲利普是一位因事故而四肢瘫痪的贵族。两人之间逐渐产生了一段意想不到的友谊：幽默、信任和尊重改变了他们的日常生活，也让人看到尊严并不取决于社会阶层。
奥马尔·希用他积极的能量和自然的表演打动了我：他能让人发笑，却从不贬低任何人；面对困难时，他也能给人勇气。他的经历证明，一个人可以在保持朴实的同时取得成功。
那么，你们又被哪位艺术家所激励呢？`
          },
          { type: "section", titleCn: "特殊题", descFr: "", descCn: "" },
          {
            id: 3, topicCn: "02-01 (Tâche 2)找运动搭子",
            promptFr: "Vous souhaitez trouver un(e) camarade pour faire du sport. Vous écrivez un message sur le site des étudiants de votre école en précisant vos horaires libres.",
            promptCn: "你想找一位同学/伙伴一起运动。你在学校的学生网站上写一条消息，并说明你空闲的时间段。",
            answerFr: `Bonjour tout le monde, j’espère que vous allez bien. Ce message a pour but de chercher un(e) camarade pour faire du sport ensemble.
Je viens de commencer mes cours de yoga dans le centre sportif situé au centre-ville de Toronto, près de notre université. Des cours encadrés par des entraîneurs professionnels sont disponibles à horaires fixes pour optimiser l’expérience sportive. Le prix est d'environ 50 dollars par mois par personne. Ce prix inclut l’accès à la salle de sport, au sauna et à la piscine. Il y a aussi un parking sur place.
Je serai libre le mardi, le jeudi et le week-end de 9 h du matin à 4 h de l’après-midi. Il est préférable que vous soyez étudiant(e) en commerce.
Si vous êtes intéressé, merci de me contacter par courriel : avfindg@gmail.com ou par téléphone : 514-000-0000.`,
            answerCn: `大家好，希望你们都过得不错。这条消息的目的是想找一位同学/伙伴一起运动。
我刚开始在多伦多市中心、靠近我们大学的体育中心上瑜伽课。这里有由专业教练带领、按固定时间安排的课程，可以帮助提升运动体验。费用大约是每人每月 50 加元。这个价格包含健身房、桑拿和游泳池的使用权。场地内也有停车位。
我每周二、周四以及周末上午 9 点到下午 4 点都有空。最好你是商科学生。
如果你感兴趣，请通过邮箱 avfindg@gmail.com或电话514-000-0000 联系我。`
          },
          { type: "section", titleCn: "题库", descFr: "", descCn: "" },
          {
            id: 4, topicCn: "02-03 (Tâche 2) 老年协会描述过去+谈感受",
            promptFr: "Vous faites partie d’une association qui soutient les personnes âgées. Écrivez un article pour un blog afin de raconter votre expérience et motiver d’autres personnes à s’engager.",
            promptCn: "你是一个支持老年人的协会成员。请为一个博客写一篇文章，讲述你的经历，并鼓励/激励其他人参与并投入志愿服务。",
            answerFr: `Bonjour tout le monde, j’espère que vous allez bien. 
Aujourd’hui, je voudrais partager une expérience inoubliable et enrichissante avec vous. La semaine dernière, j’ai participé à une activité bénévole dans une association qui soutient les personnes âgées. Cette activité était organisée pour cultiver la solidarité et sensibiliser le public à l’importance du bien-être physique et moral. Concrètement, j’ai accompagné une personne âgée lors d’une promenade, puis nous avons discuté autour d’un café ; j’ai aussi aidé à organiser une petite activité de groupe pour créer du lien. 
Ayant participé à cette activité, je trouve que mon expérience s’est considérablement enrichie. Elle m’a permis d’améliorer ma communication, mon écoute et mon empathie, tout en renforçant ma confiance en moi. S’engager, même une heure par semaine, peut vraiment faire une différence dans la vie de quelqu’un. 
En conclusion, je recommande vivement à tout le monde de vivre une expérience comme celle-ci. 
Haoyan
`,
            answerCn: `大家好，希望你们都过得不错。
今天我想和大家分享一段难忘而且很有收获的经历。上周，我参加了一项由支持老年人的协会组织的志愿活动。此次活动旨在培养互助精神，并让公众意识到身心健康的重要性。具体来说，我陪一位老人散步，之后我们在咖啡馆边喝咖啡边聊天；我也帮忙组织了一场小型团体活动，促进彼此交流与建立联系。
参加了这次活动后，我觉得自己的经历得到了很大的丰富与提升。它让我在提升沟通能力的同时，也加强了倾听与共情能力，并增强了自信。即使每周只投入一小时的时间，也真的能给他人的生活带来改变。
总之，我强烈推荐大家去体验一次这样的活动。
Haoyan
`
          },
          {
            id: 5, topicCn: "02-04 (Tâche 2) 旅游描述过去+谈感受",
            promptFr: "Vous avez effectué un séjour au Canada grâce à une agence de voyages. Rédigez un commentaire pour décrire l’expérience que vous avez vécue pendant ce voyage.",
            promptCn: "你通过一家旅行社在加拿大进行了一次旅行。请写一则评论，描述你在这次旅行中经历的体验。",
            answerFr: `Bonjour tout le monde, j’espère que vous allez bien. 
Aujourd’hui, je voudrais partager une expérience inoubliable et enrichissante avec vous. La semaine dernière, j’ai voyagé à Toronto grâce à une agence de voyages. Toronto est une ville moderne, connue pour ses gratte-ciels, sa diversité culturelle et sa vitalité économique. Au total, j’ai visité la tour CN, l’Université de Toronto et le Musée royal de l’Ontario. L’organisation était claire et le programme bien rythmé, ce qui m’a permis de profiter pleinement du séjour. Pendant ce voyage, j’ai découvert une nouvelle culture, pratiqué la langue au quotidien et goûté à des spécialités étrangères, ce qui m’a vraiment ouvert l’esprit. Cette expérience m’a aussi donné plus de confiance en moi et m’a rendu plus autonome. 
En conclusion, je recommande vivement à tout le monde de vivre une expérience comme celle-ci. 
Haoyan
`,
            answerCn: `大家好，希望你们都过得不错。
今天我想和大家分享一段难忘而且很有收获的经历。上周，我通过一家旅行社去了多伦多旅行。多伦多是一座现代化城市，以摩天大楼、文化多元和经济活力而闻名。我一共参观了加拿大国家电视塔（CN 塔）、多伦多大学以及安大略皇家博物馆。旅行安排清晰、行程节奏合理，让我能充分地享受这次旅程。
在这次旅行中，我接触了新的文化，日常练习语言，还品尝了各种异国美食，这真的让我开阔了眼界。这段经历也让我更加自信，并变得更独立。
总之，我强烈推荐大家体验一次这样的旅行。
Haoyan
`
          },
          {
            id: 6, topicCn: "02-05 (Tâche 2) 度假描述过去+谈感受",
            promptFr: "Vous revenez d’une journée passée à la campagne avec vos amis. Vous publiez un message sur votre forum pour partager votre expérience et décrire ce que vous avez aimé (activités, paysages, animaux, etc.).",
            promptCn: "你刚和朋友们在乡村度过了一天。你要在论坛上发一条帖子，分享你的经历，并描述你喜欢的部分（活动、风景、动物等）。",
            answerFr: `Bonjour tout le monde, j’espère que vous allez bien. 
Aujourd’hui, je voudrais partager une expérience inoubliable et enrichissante avec vous. Le samedi dernier, j’ai passé une journée à la campagne avec mes amis, dans une ferme. Au programme, il y avait plusieurs activités : arroser les plantes, nourrir les animaux (poules, chèvres et vaches) et nettoyer les enclos. Entre deux tâches, nous avons aussi fait une petite promenade au milieu des champs et profité du calme et de l’air frais. 
Ayant participé à cette expérience, je trouve que cette journée m’a beaucoup apporté. Tout d’abord, après ces activités, mon stress a fortement diminué. De plus, cette sortie m’a rappelé l’importance de protéger l’environnement et la biodiversité. 
En conclusion, je recommande vivement à tout le monde de vivre une expérience comme celle-ci. 
Haoyan
`,
            answerCn: `大家好，希望你们都过得不错。
今天我想和大家分享一段难忘而且很有收获的经历。上周六，我和朋友们在乡下的一家农场度过了一整天。活动安排有很多：给植物浇水、喂动物（鸡、山羊和奶牛），以及清理圈舍。在两项任务之间，我们还在田野间散步，享受宁静的氛围和清新的空气。
参加了这次体验后，我觉得这一天带给我很多收获。首先，做完这些活动后，我的压力明显减轻了。此外，这次出行也让我意识到保护环境和生物多样性的重要性。
总之，我强烈推荐大家去体验一次这样的活动。
Haoyan
`
          },
          {
            id: 7, topicCn: "02-06 (Tâche 2) 音乐描述过去+谈感受",
            promptFr: ` École de musique !
Activités gratuites, concerts et jeux.
Rendez-vous vendredi dès 9 heures. »
Vous avez pris part à cet événement. Vous adressez un message à vos amis pour décrire ce que vous avez vécu et exprimer votre avis sur cette journée.
`,
            promptCn: `音乐学校！
免费活动、音乐会和游戏。
周五早上9点开始集合。
你参加了这次活动。你要给朋友们发一条消息，描述你当天的经历，并表达你对这一天的看法。
`,
            answerFr: `Bonjour tout le monde, j’espère que vous allez bien. 
Aujourd’hui, je voudrais partager une expérience inoubliable et enrichissante avec vous. Vendredi dernier, dès 9 h, je suis allé à l’école de musique de ma ville. Au programme : ateliers de chant et de piano, un concert rock gratuit, un concert classique et un quiz sur les comédies musicales. 
Ayant participé à cet événement, je trouve que mon expérience s’est considérablement enrichie. Tout d'abord, après avoir assisté à ces concerts, mon stress a fortement diminué. Ensuite, en participant à cette activité, j’ai découvert un univers musical différent et cela m’a ouvert l’esprit. De plus, ce genre d’activité nous offre une belle opportunité pour partager un moment inoubliable avec nos proches. 
En conclusion, je recommande vivement à tout le monde de vivre une expérience comme celle-ci.
Haoyan
`,
            answerCn: `大家好，希望你们都过得不错。
今天我想和大家分享一段难忘而且很有收获的经历。上周五从早上 9 点开始，我去了我所在城市的音乐学校。活动安排包括：声乐和钢琴工作坊、一场免费的摇滚音乐会、一场古典音乐会，以及一个关于音乐剧的知识问答。
参加了这次活动后，我觉得自己的经历得到了很大的丰富与提升。首先，听完这些音乐会后，我的压力明显减轻了。其次，通过参加这次活动，我发现了一个不同的音乐世界，这让我更加开阔了眼界。此外，这类活动也为我们提供了一个很好的机会，可以和亲友一起分享难忘的时光。
总之，我强烈推荐大家去体验一次这样的活动。
Haoyan
`
          },
          {
            id: 8, topicCn: "02-07 (Tâche 2) 旧货市场描述过去+谈感受",
            promptFr: "Vous avez pris part à un marché d’occasion dans votre ville. Rédigez un article sur votre blog pour raconter cette activité et dire pourquoi elle vous a plu.",
            promptCn: "你参加了你所在城市的一个二手市集。请在你的博客上写一篇文章，讲述这次活动，并说明你为什么喜欢它。",
            answerFr: `Bonjour tout le monde, j’espère que vous allez bien. 
Aujourd’hui, je voudrais partager une expérience inoubliable et enrichissante avec vous. La semaine dernière, j’ai participé à un marché d’occasion dans ma ville. Au programme, il y avait la vente d’objets de seconde main, la réutilisation de vieux objets et la sensibilisation à l’environnement. J’ai parcouru plusieurs stands, discuté avec des vendeurs, comparé les prix et même négocié pour certains articles. 
Ayant participé à cet événement, je trouve que mon expérience s’est considérablement enrichie. Tout d’abord, j’ai pu faire des économies tout en trouvant des objets utiles. Ensuite, l’ambiance conviviale m’a aidé à améliorer ma communication et mon sens de la négociation. Finalement, cette journée m’a donné plus de confiance en moi et m’a rendu plus autonome dans mes choix de consommation. En conclusion, je recommande vivement à tout le monde de vivre une expérience comme celle-ci.
Haoyan 
`,
            answerCn: `大家好，希望你们都过得不错。
今天我想和大家分享一段难忘而且很有收获的经历。上周，我参加了我所在城市的一个二手市集。活动内容包括售卖二手物品、旧物再利用以及环保意识宣传。我逛了好几个摊位，和卖家聊天、比较价格，甚至还为一些商品讨价还价。
参加了这次活动后，我觉得自己的经历得到了很大的丰富与提升。首先，我既省了钱，又找到了实用的物品。其次，友好热闹的氛围帮助我提升了沟通能力和议价技巧。最后，这一天让我更有自信，也让我在消费选择上变得更独立、更自主。总之，我强烈推荐大家去体验一次这样的活动。
Haoyan
`
          },
          {
            id: 9, topicCn: "02-10 (Tâche 2) 美食比赛描述过去+谈感受",
            promptFr: "Vous avez pris part à une compétition culinaire. Sur votre site web, vous rédigez un petit article pour décrire le déroulement de la journée. Vous précisez les raisons pour lesquelles cette expérience vous a plu ou non.",
            promptCn: "你参加了一场烹饪比赛。你要在自己的网站上写一篇简短的文章，描述当天的活动流程，并说明你喜欢或不喜欢这次经历的原因。",
            answerFr: `Bonjour tout le monde, j’espère que vous allez bien. Aujourd’hui, je voudrais partager une expérience inoubliable et enrichissante avec vous.
La semaine dernière, j’ai participé avec ma famille à une compétition culinaire. Au programme, il y avait les cuisines traditionnelles de différents pays et cultures et la dégustation du vin rouge et du fromage.  
Ayant participé à ce concours, je trouve que mon expérience s’est considérablement enrichie. Tout d’abord, j’ai goûté des spécialités étrangères et acquis une meilleure compréhension du monde. Ensuite, grâce aux échanges avec les nouveaux amis que j’ai rencontrés, j’ai découvert des perspectives différentes et cela m’a permis d’élargir mon horizon. Finalement, cette expérience m’a permis de gagner en confiance en moi et de devenir plus autonome.
En conclusion, je recommande vivement à tout le monde de vivre une expérience comme celle-ci.
`,
            answerCn: `大家好，希望你们都过得不错。今天我想和大家分享一段难忘而且很有收获的经历。
上周，我和家人一起参加了一场烹饪比赛。活动内容包括来自不同国家和文化的传统菜肴，以及红酒和奶酪的品尝。
参加了这次比赛后，我觉得自己的经历得到了很大的丰富与提升。首先，我品尝了各国特色美食，对世界有了更深入的了解。其次，通过和我认识的新朋友交流，我看到了不同的观点，这也让我开阔了眼界。最后，这次经历让我更加自信，也让我变得更独立、更自主。
总之，我强烈推荐大家去体验一次这样的活动。
`
          },
        ];

"""

# ---- Config ----
TACHE = 2             # change to 2/3 if you want
KIND = "a"               # "a" for answers; if you insist, change to "q"
OUT_CSV = Path("assets/tcfEE/t2.csv")
# ----------------

import re

def extract_answerfr_strings(text: str) -> list[str]:
    # matches: answerFr: `...`   OR   answerFr: "..."
    pat = re.compile(
        r'answerFr\s*:\s*(?:`(?P<bt>[\s\S]*?)`|"(?P<dq>(?:\\.|[^"\\])*)")'
    )

    answers = []
    for m in pat.finditer(text):
        s = m.group("bt") if m.group("bt") is not None else m.group("dq")
        # if it's the "..." form, unescape (optional but nice)
        if m.group("dq") is not None:
            s = bytes(s, "utf-8").decode("unicode_escape")
        s = (s or "").strip()
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
