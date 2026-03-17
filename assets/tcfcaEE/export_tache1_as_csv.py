#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 [
          {

            id: 1, topicCn: "01-03旅行+传统节日",
            promptFr: "Un de vos proches souhaite partir en voyage pour découvrir un nouveau pays. Vous lui envoyez un message pour lui présenter votre pays et ses traditions (lieux à visiter, sites touristiques, monuments, etc.).",
            promptCn: "你的一个亲友想去旅行，去发现一个新的国家。你给他/她发一条消息，向他/她介绍你的国家及其传统（可以参观的地方、旅游景点、纪念碑/名胜古迹等）。",
            answerFr: `Cher Hao,
Je t’écris pour te recommander de passer tes prochaines vacances à Toronto, au Canada, en été, parce que dans ta dernière lettre tu as mentionné que tu voulais découvrir un nouveau pays. Cette ville offre de nombreux sites qui valent le détour, comme la tour CN,  l’Université de Toronto et le Musée royal de l’Ontario. Nous pourrions y découvrir l’histoire et les cultures du Canada. En juillet, tu pourras aussi célébrer la fête du Canada avec ses feux d’artifice et ses concerts.
Si tu veux, je viendrai te chercher à l’aéroport et nous pourrons loger ensemble, car les hôtels du centre-ville sont chers.
Écris-moi si cette proposition t’intéresse, pour que je puisse mieux organiser ce voyage pour toi.
Bises,
Haoyan`,
            answerCn: `亲爱的Hao：
我写信是想推荐你在夏天来加拿大多伦多度过你的下一个假期，因为你在上一封信里提到你想去发现一个新的国家。这座城市有很多值得一看的景点，比如CN塔、多伦多大学和安大略皇家博物馆。我们还可以在这里了解加拿大的历史和文化。到了七月，你也可以参加加拿大国庆庆祝活动，包括烟花和音乐会。
            如果你愿意，我可以去机场接你，我们也可以一起住，因为市中心的酒店很贵。
            如果你对这个提议感兴趣，请给我回信，这样我就能更好地为你安排这次旅行。
            亲吻/ 祝好，
          Haoyan`
          },
          {
            id: 2, topicCn: "01-04周末出行计划",
            promptFr: "Vous souhaitez organiser un week-end avec vos proches le mois prochain. Vous envoyez un message pour leur expliquer votre plan, en décrivant le lieu, le moyen de transport et les activités prévues.",
            promptCn: "你想在下个月和亲友一起组织一个周末活动。你发送一条消息向他们说明你的计划，包括地点、交通方式以及安排的活动。",
            answerFr: `Chers proches,
Je vous écris afin de vous proposer de passer un week-end avec moi le mois prochain. J’aimerais organiser une escapade au parc national de Banff le 5 mars.
Dans un premier temps, nous nous retrouverons devant mon appartement à 9 h du matin. Puis, nous nous rendrons sur place en transports en commun, notamment en métro et en bus, car c’est pratique et écologique.
En ce qui concerne les activités prévues, nous pourrons faire de la randonnée, du vélo et du ski. Le soir, nous passerons la nuit à l’hôtel Rose, qui propose des chambres confortables à un prix raisonnable.
N’hésitez pas à me dire si vous êtes disponibles.
À bientôt,
Haoyan`,
            answerCn: `我写这封信是想邀请你们下个月和我一起度过一个周末。我想在 3 月 5 日组织一次前往班夫国家公园的小旅行。
首先，我们会在早上 9 点在我公寓门口集合。然后，我们将乘坐公共交通前往目的地，主要是地铁和公交车，因为这样既方便又环保。
至于计划的活动，我们可以去徒步、骑自行车和滑雪。晚上，我们会住在 Rose 酒店过夜，这家酒店提供舒适的房间，价格也比较合理。
如果你们有时间，请告诉我。
期待很快见到你们！
Haoyan`
          },
          {
            id: 3, topicCn: "11-04运动",
            promptFr: "Envoyez un message à vos amis pour les inviter à passer un week-end chez vous et pratiquer ensemble des activités sportives.",
            promptCn: "给你的朋友们发一条消息，邀请他们来你家过周末，并一起进行体育活动。",
            answerFr: `Cher Hao, 
Je t’écris pour te proposer de passer le week-end prochain chez moi. J’aimerais que nous pratiquions ensemble des activités sportives. 
Samedi, nous visiterons au centre sportif : nous pourrons faire plusieurs activités, par exemple le tennis, la natation et le yoga. Dimanche, nous ferons une promenade à Queens Park. 
Tu peux venir chez moi vendredi soir. Pendant le week-end, nous nous déplacerons en transports en commun, un choix à la fois pratique et écologique. 
Écris-moi dès que possible si tu es disponible, afin que je puisse réserver à l’avance. 
Haoyan`,
            answerCn: `亲爱的 Hao：
我写信是想邀请你下个周末来我家一起过。我希望我们能一起做一些体育活动。
星期六，我们会去体育中心：我们可以进行多种活动，比如网球、游泳和瑜伽。星期天，我们会去 Queen’s Park 散步。
你可以周五晚上就来我家。周末期间，我们会乘坐公共交通出行，这既方便又环保。
如果你有时间，请尽快回复我，这样我可以提前预订。
Haoyan`
          },
          {
            id: 4, topicCn: "11-10见作家",
            promptFr: "Rédigez un message à un ami pour l’inviter à une rencontre avec un écrivain organisée par la bibliothèque de votre ville.",
            promptCn: "给一位朋友写一条消息，邀请他/她参加由你所在城市的图书馆组织的一场作家见面会。",
            answerFr: `Cher Hao,
Je t’écris pour t’inviter à une rencontre avec un écrivain le 1er juillet, organisée par la bibliothèque de ma ville.
On se retrouvera d’abord devant l’Université de Toronto à 10h du matin. Nous visiterons la bibliothèque dans la matinée. Nous profiterons de cette journée en participant à plusieurs activités culturelles : une discussion avec l’écrivain, et peut-être des expositions. L’après-midi, nous pourrions aller au musée d’histoire en face de la bibliothèque. Si le temps le permet, nous pourrions aussi manger dans un restaurant chinois à Chinatown. Nous nous déplacerons en transports en commun, car c’est un moyen pratique et écologique.
Écris-moi si tu es disponible pour que je puisse faire des réservations à l’avance.
À bientôt,
Haoyan`,
            answerCn: `亲爱的 Hao：
我写信是想邀请你参加由我所在城市的图书馆组织的一场作家见面会，时间是 7 月 1 日。
我们会先在早上 10 点在多伦多大学门口集合。上午我们将参观图书馆。我们会参加多项文化活动：与作家交流讨论，以及可能还有一些展览。下午，我们可以去图书馆对面的历史博物馆。如果时间允许，我们也可以去唐人街的一家中餐馆吃饭。我们将乘坐公共交通出行，因为这既方便又环保。
如果你有时间，请告诉我，这样我可以提前预订。
期待见到你！
Haoyan`
          },
          {
            id: 5, topicCn: "8-10游乐园",
            promptFr: "Parc de loisirs : J'ai hâte de profiter de cette journée avec toi demain ! Peux-tu me dire quelles activités sont au programme ? Écrivez un message pour répondre à votre ami(e).",
            promptCn: "游乐园：我迫不及待想明天和你一起享受这一天！你能告诉我都安排了哪些活动吗？请写一条消息回复你的朋友。",
            answerFr: `Cher Hao, 
Je suis ravi que tu m’accompagnes demain au parc de loisir ! 
Je te donne les détails suivants : on se retrouvera d’abord devant la bibliothèque municipale à 9 h, puis nous prendrons le métro, un choix à la fois pratique et écologique. Nous arriverons au parc vers 9 h 30. Au programme, il y aura des montagnes russes, la grande roue, des maisons hantées et des spectacles. Nous pourrions déjeuner sur place. Nous quitterons le parc en fin d’après-midi, selon ton énergie. 
Écris-moi dès que possible pour me confirmer que tout est bon, afin que je puisse réserver les billets à l’avance. 
Haoyan`,
            answerCn: `亲爱的 Hao：
我很高兴你明天能陪我一起去游乐园！
我把具体安排告诉你：我们先在早上 9 点在市立图书馆门口集合，然后乘地铁过去，这既方便又环保。我们大约 9 点 30 分到达游乐园。活动安排有过山车、摩天轮、鬼屋和各种表演。我们可以在园内吃午饭。下午晚些时候我们就离开，具体时间看你的精力/体力情况。
请尽快回复我确认一切都没问题，这样我可以提前订票。
Haoyan`
          },
          {
            id: 6, topicCn: "08-08电影节",
            promptFr: "Vous voulez aller à un festival de films dans votre ville. Rédigez un message à un ami pour lui proposer de vous accompagner. Indiquez clairement les détails de l’événement (films, horaires, dates et prix).",
            promptCn: "你想去你所在城市的一个电影节。请给一位朋友写一条消息，邀请他/她陪你一起去。请清楚写明活动细节（电影内容/类型、时间安排、日期和票价）。",
            answerFr: `Cher Hao,
Je t'écris pour t'inviter à aller à un festival de films qui se situe à la bibliothèque municipale avec moi le 23 mai.
Comme il aura lieu de 10h à 18h, on se retrouvera d'abord devant mon appartement à 9h30 et nous nous déplacerons en transports en commun. Pendant ce festival, nous pourrons regarder gratuitement plusieurs films comme <Titanic>. Nous pourrions aussi rencontrer de nombreux acteurs célèbres.  
Le billet coûte seulement 20 dollars par personne. Je suis sûr que ce sera un événement inoubliable. Écris-moi vite si tu es disponible!
À bientôt,
Haoyan`,
            answerCn: `亲爱的 Hao：
我写信是想邀请你在 5 月 23 日和我一起去市立图书馆举办的电影节。
由于活动时间是上午 10 点到下午 6 点，我们先在早上 9 点 30 分在我公寓门口集合，然后乘坐公共交通前往。电影节期间，我们可以免费观看多部电影，比如《泰坦尼克号》。我们还可能见到许多著名演员。
门票每人只要 20 美元/加元。我相信这会是一场难忘的活动。若你有时间，快回我消息吧！
回头见，
Haoyan`
          },
          { type: "section", titleCn: "生日派对", descFr: "", descCn: "" },
          {
            id: 7, topicCn: "10-03生日保密",
            promptFr: "Vous rédigez un message à vos amis pour les convier à une fête d’anniversaire surprise organisée pour votre meilleur(e) ami(e). Indiquez le lieu, la date et l’heure, etc.",
            promptCn: "你给朋友们写一条消息，邀请他们参加为你最好的朋友举办的惊喜生日派对。请注明地点、日期、时间等细节。",
            answerFr: `Chers amis,
Je vous écris pour vous inviter à fêter l'anniversaire surprise de mon meilleur ami, Li Hua, ensemble le 5 mai.
La soirée se déroulera dans son restaurant préféré, Quanjude. Il se situe au centre-ville de Toronto, à côté du marché Byward. Comme il propose un grand stationnement gratuit juste devant l'entrée, vous pourrez venir en voiture.
On va tout préparer à l'avance : le menu, la décoration et les activités après le dîner. La fête aura lieu à 20h. Si vous voulez aider à l’organisation, arrivez à 4h de l’après-midi. Gardez bien le secret, parce que c'est un événement surprise !
Merci de me confirmer votre présence pour que je puisse réserver.
À bientôt,
Haoyan`,
            answerCn: `亲爱的朋友们：
我写这封信是想邀请大家在 5 月 5 日一起参加为我最好的朋友李华准备的惊喜生日派对。
聚会将在他最喜欢的餐厅——全聚德——举行。餐厅位于多伦多市中心，紧挨着 Byward 市场。因为餐厅入口前有一个大型免费停车场，你们可以开车前来。
我们会提前把一切都准备好：菜单、装饰以及晚饭后的活动。派对将在晚上 8 点开始。如果你想帮忙筹备，请在下午 4 点到达。一定要保密，因为这是一个惊喜活动！
请确认你是否能来，以便我预订座位。
期待见到大家！
Haoyan`
          },
          { type: "section", titleCn: "地点场所描述", descFr: "", descCn: "" },
          {
            id: 8, topicCn: "10-04介绍新公寓",
            promptFr: "Vous avez récemment déménagé dans une autre ville. Rédigez un message à un(e) ami(e) pour lui parler de votre nouveau lieu de résidence (quartier, habitants, magasins, etc.).",
            promptCn: "你最近搬到了另一个城市。请给一位朋友写一条消息，向他/她介绍你新的居住地（社区/街区、居民情况、商店等）。",
            answerFr: `Cher Hao,
Je t’écris pour te donner des nouvelles de mon nouveau logement.
J’ai déménagé dans mon nouvel appartement il y a un mois. C’est un deux-pièces situé au centre-ville de Toronto, dans un quartier calme et agréable. Il est entouré de nombreux commerces et services de proximité, comme des cafés, des supermarchés et des parcs.
L’endroit que je préfère est le café près de chez moi, car il est spacieux et bien décoré. J’aime y passer mes après-midis à lire ou à déguster un café. Mes voisins sont sympathiques et nous nous entendons bien.
Je t’invite à passer un week-end chez moi. Écris-moi si tu es disponible.
À bientôt,
Haoyan`,
            answerCn: `亲爱的 Hao:
我写信是想告诉你一些关于我新住处的消息。
我一个月前搬进了新公寓。这是一套位于多伦多市中心的两居室，所在社区安静又舒适。周围有很多商店和便民服务，比如咖啡馆、超市和公园。
我最喜欢的地方是我家附近的那家咖啡馆，因为那里空间很大、装修也很漂亮。我喜欢在那儿度过下午时间，读书或者品尝咖啡。邻居们也很友好，我们相处得很好。
我邀请你来我家过一个周末。如果你有时间就给我回个消息。
回头见，
Haoyan`
          },
          {
            id: 9, topicCn: "10-02新工作",
            promptFr: "« Salut, Tu as commencé ton nouveau boulot ! Comment ça se passe ? Es-tu satisfait(e)? Ali » Répondez à Ali en lui parlant de votre nouveau poste (lieu, collègues…) et en donnant votre avis.",
            promptCn: "“嗨，你开始新工作了！进展怎么样？你满意吗？——Ali”请回复 Ali，向他/她介绍你的新职位（工作地点、同事等），并表达你的看法/评价。",
            answerFr: `Cher Ali,
Je t’écris pour te donner des nouvelles de mon nouveau travail.
J’ai commencé un poste dans une entreprise spécialisée dans la fabrication de meubles. Elle est située à côté d’IKEA,  au centre-ville de Vancouver, ce qui me permet d’y accéder facilement en transports en commun.
Je suis satisfait de mon nouvel environnement professionnel, car mes collègues et moi nous nous entendons bien. Ils m’aident à améliorer ma technique et je partage parfois mon déjeuner avec eux.
Je t’invite à passer à mon atelier afin de te faire une petite table. Écris-moi si tu es disponible.
À bientôt,
Haoyan`,
            answerCn: `亲爱的 Ali：
我写信是想告诉你一些我新工作的近况。
我在一家专门生产家具的公司开始了一份新工作。公司位于温哥华市中心、IKEA 旁边，这让我可以很方便地乘坐公共交通到达。
我对新的工作环境很满意，因为我和同事们相处得很好。他们帮助我提升技术，我也有时会和他们一起分享午餐。
我也邀请你来我的工作室参观，我可以给你做一张小桌子。如果你有时间就告诉我。
回头见，
Haoyan`
          },
          {
            id: 10, topicCn: "01-02新学校",
            promptFr: "« Salut, J’espère que tu vas bien. Dis-moi, que penses-tu de ta nouvelle université ? Est-ce que l’ambiance avec les étudiants est bonne ? Comment trouves-tu les professeurs ? À très bientôt. Martin » Vous écrivez un message à Martin dans lequel vous présentez votre université (les professeurs, les étudiants, les activités, etc.).",
            promptCn: "“嗨！希望你一切都好。跟我说说，你觉得你的新大学怎么样？你和同学们相处的氛围好吗？你觉得老师/教授怎么样？很快见。Martin”请你给 Martin 写一条消息，在其中介绍你的大学（教授、学生、活动等方面）。",
            answerFr: `Cher Martin,
Je t’écris pour te donner de mes nouvelles. Je viens de commencer mes cours dans ma nouvelle université située au centre-ville de Vancouver. Le campus est bien équipé avec une bibliothèque, un centre sportif et une cantine, ce qui me permet de participer à différentes activités pendant mon temps libre: le tennis, la natation et  l’escalade.
Je suis satisfait de mon nouvel environnement, car mes professeurs, mes camarades et moi, nous nous entendons bien. Au début de mes cours, je n’étais pas capable de les comprendre à 100 % à cause des différences culturelles. Heureusement, ils étaient très patients et ils m’ont beaucoup aidé.
Et toi, as-tu des nouvelles à me donner ? Écris-moi !
Haoyan`,
            answerCn: `亲爱的 Martin：
我写信是想告诉你我的近况。我刚开始在位于温哥华市中心的新大学上课。校园设施很完善，有图书馆、体育中心和食堂，这让我能在空闲时间参加不同的活动，比如网球、游泳和攀岩。
我对新的环境很满意，因为我和老师、同学们相处得很好。刚开始上课时，由于文化差异，我没办法百分之百听懂他们在讲什么。幸运的是，他们都很有耐心，也给了我很多帮助。
你呢？有什么近况想跟我分享吗？给我写信吧！
Haoyan`
          },
          {
            id: 11, topicCn: "11-01酒店",
            promptFr: "Vous comptez partir en vacances avec vos amis et vous avez repéré un hôtel intéressant. Vous rédigez un message pour leur donner des détails sur cet hôtel (emplacement, tarif, services, etc.) et vous leur suggérez de faire la réservation.",
            promptCn: "你打算和朋友一起去度假，并找到了一个不错的酒店。你写一条消息向他们介绍这家酒店的细节（位置、价格、服务等），并建议他们进行预订。",
            answerFr: `Cher Hao, 
Je t’écris pour te donner des détails sur l’hôtel que j’ai repéré.
Je viens de trouver un hôtel parfait pour nos vacances et je vous recommande vivement de faire une réservation. Il se situe au centre-ville de Toronto, avec beaucoup de commerces et de services à proximité : des parcs, des supermarchés, un grand magasin, un cinéma, des écoles, un centre sportif et une bibliothèque. 
Le prix est d’environ 500 $ par nuit et par personne. Ce prix inclut l’accès à une salle de sport, un sauna et une piscine, ainsi que trois repas par jour. Il y a aussi un parking sur place. 
Si tu as d’autres questions, n’hésite pas à m’appeler. 
Haoyan`,
            answerCn: `亲爱的 Hao：
我写信是想告诉你我看中的那家酒店的一些细节。
我刚找到一家非常适合我们度假的酒店，我强烈建议你们尽快预订。它位于多伦多市中心，附近有很多商店和便民服务：公园、超市、大型商场、电影院、学校、体育中心和图书馆。
价格大约是每人每晚 500 加元。这个价格包含健身房、桑拿和游泳池的使用权，以及每天三顿餐食。酒店还提供停车位。
如果你还有其他问题，随时给我打电话。
Haoyan`
          },
          {
            id: 12, topicCn: "11-02健身房",
            promptFr: "« Bonjour ! J’ai entendu dire que tu pratiques une activité sportive depuis le mois dernier. Ça m’intéresse et j’aimerais t’accompagner. Tu peux me donner plus de détails ? À bientôt ! Camille » Vous écrivez une réponse à votre ami(e) Camille. Dans votre message, vous présentez votre sport et indiquez des détails pratiques (endroit, temps, coût, etc.). ",
            promptCn: "“你好！我听说你从上个月开始在练一项运动。我很感兴趣，也想和你一起参加。你能给我更多细节吗？回头见！Camille”你要给朋友（Camille）写一封回复。在信息中介绍你做的运动，并说明一些实际细节（地点、时间、费用等）。",
            answerFr: `Salut Camille,
Je t’écris pour te répondre à ta question concernant le sport que je pratique maintenant.
Je viens de commencer mes cours de yoga dans le centre sportif situé au centre-ville de Toronto, près de mon nouvel appartement. Il est ouvert 24 heures sur 24 et 7 jours sur 7. Des cours encadrés par des entraîneurs professionnels sont disponibles à horaires fixes pour optimiser ton expérience sportive.
Le prix est d'environ 100 dollars par mois par personne. Ce prix inclut l’accès à la salle de sport, au sauna et à la piscine. Il y a aussi un parking sur place.
Si tu veux, je t’invite à prendre un cours d'essai, car le premier cours est offert.
Haoyan`,
            answerCn: `嗨 Camille：
我写信是为了回复你关于我现在在练的运动的问题。
我刚开始在多伦多市中心的一家体育中心上瑜伽课，它就在我新公寓附近。该中心每周 7 天、每天 24 小时开放。为了让你的运动体验更好，这里还提供由专业教练带领、按固定时间安排的课程。
费用大约是每人每月 100 加元。这个价格包含健身房、桑拿和游泳池的使用权。场地内也有停车位。
如果你愿意的话，我邀请你来上一节体验课，因为第一节课是免费的。
Haoyan`
          },
          {
            id: 13, topicCn: "03-02语言学校",
            promptFr: "Rédiger un message à un ami intéressé par des cours de langue dans votre école, en lui fournissant des informations utiles sur les programmes proposés, les tarifs et le lieu.",
            promptCn: "给一位对你学校语言课程感兴趣的朋友写一条消息，向他/她提供有用信息：学校提供哪些课程/项目、费用多少、上课地点在哪里。",
            answerFr: `Cher Hao,
Je t’écris pour te répondre à ta question concernant les cours de langue dans mon école. Je viens de commencer mes cours dans une école de langues au centre-ville de Toronto. Comme elle se trouve en plein centre, il est facile d’y accéder en transports en commun. L’école propose plusieurs programmes : l’anglais, le français, le chinois, etc. Les frais s’élèvent à 8 999 $ pour un programme de huit mois. L’ambiance est très bonne : mes camarades et moi, nous nous entendons bien. 
Si tu as d’autres questions, n’hésite pas à m’appeler. 
Haoyan`,
            answerCn: `亲爱的 Hao：
我写信是为了回复你关于我学校语言课程的问题。我刚开始在多伦多市中心的一所语言学校上课。因为学校位于市中心，乘坐公共交通很容易到达。学校提供多种课程项目：英语、法语、中文等。八个月的课程费用是 8,999 加元。学校氛围很好：我和同学们相处得很融洽。
如果你还有其他问题，随时给我打电话。
Haoyan`
          },
          { type: "section", titleCn: "住房相关", descFr: "", descCn: "" },
          {
            id: 14, topicCn: "11-11找室友",
            promptFr: "Vous venez d’emménager dans un nouvel appartement et vous cherchez un(e) colocataire. Vous rédigez une annonce en donnant toutes les informations sur le logement (emplacement, superficie, loyer, etc.) et en décrivant la personne avec qui vous souhaiteriez partager l’appartement (caractère, habitudes, mode de vie, etc.).",
            promptCn: "你刚搬进一套新公寓，正在寻找一位室友。请你写一则招室友的广告，提供住房的所有信息（位置、面积、租金等），并描述你希望一起合租的人（性格、习惯、生活方式等）。",
            answerFr: `Bonjour,
Cette annonce a pour but de chercher un colocataire. Je viens d'emménager dans un appartement de deux pièces situé au centre-ville de Toronto, dans un quartier calme. L'appartement fait 800 pieds carrés et comprend deux chambres, une cuisine, un salon ainsi qu'une salle de bains. Le loyer s'élève à 2000 euros par mois par personne, charges comprises. Cet immeuble est entouré par plusieurs commodités publiques, comme les supermarchés et les restaurants.
J'aimerais que vous soyez une personne sérieuse, propre et non-fumeur. Je préférerais également que nous puissions avoir un rythme de vie similaire : je me lève vers 8h et me couche à minuit.
Si vous êtes intéressé, veuillez me contacter par courriel : 123@gmail.com.
Meilleures salutations,
Haoyan`,
            answerCn: `你好：
这则公告旨在寻找一位合租室友。我刚搬进一套位于多伦多市中心、环境安静社区的两居室公寓。公寓面积为 800 平方英尺，包含两间卧室、一个厨房、一个客厅以及一间浴室。房租为每人每月 2000 欧元，包含水电等各项杂费。这栋楼周围有多种公共配套设施，例如超市和餐馆。
我希望你是一个认真、爱干净且不吸烟的人。我也希望我们的作息相近：我大约早上 8 点起床，午夜 12 点睡觉。
如果你感兴趣，请通过电子邮件联系我：123@gmail.com。
此致敬礼，
Haoyan`
          },
          {
            id: 15, topicCn: "09-01求租房屋",
            promptFr: "Vous prévoyez d’habiter à Nice. Rédigez un message à une agence immobilière pour rechercher un appartement ou une maison. Précisez vos critères (superficie, prix, localisation, nombre de chambres, etc.)",
            promptCn: "你计划在尼斯（Nice）居住。请给一家房产中介写一条消息，寻找一套公寓或房子，并说明你的要求（面积、价格、位置、卧室数量等）。",
            answerFr: `Bonjour,
Je vous écris afin de demander votre aide pour chercher un logement. Je prévois de déménager au début mars au centre-ville de Nice, dans un quartier calme. L’appartement devrait faire au moins 800 pieds carrés. Il est préférable qu’il y ait deux chambres, une cuisine, un salon et une salle de bains. Je souhaiterais que le loyer soit entre 1500 et 1800 euros par mois, dépenses incluses. 
Si vous avez des nouvelles concernant le logement que je cherche, veuillez m’écrire.
Haoyan`,
            answerCn: `你好：
我写信是想请您帮忙找房。我计划在三月初搬到尼斯市中心一个安静的街区。公寓面积希望至少有 800 平方英尺。最好有两间卧室、一个厨房、一个客厅和一间浴室。我希望月租在 1500 到 1800 欧元之间，并包含各项费用。
如果您有符合我需求的房源信息，请给我回信。
Haoyan`
          },
          {
            id: 16, topicCn: "11-12搬家",
            promptFr: "Vous préparez votre déménagement et vos amis ont accepté de vous aider. Vous rédigez un message groupé pour leur donner toutes les informations pratiques : lieux, horaires, durée, trajet et tâches à réaliser.",
            promptCn: "你正在准备搬家，你的朋友们也同意来帮忙。请你写一条群发消息，向他们提供所有实用信息：集合地点、时间安排、预计时长、路线/行程，以及需要完成的任务。",
            answerFr: `Chers amis, 
Merci encore d’avoir accepté de m’aider pour mon déménagement, qui aura lieu le 5 mai. Mon nouvel appartement se situe au 1410 et se trouve à environ 20 minutes de mon ancien logement. 
On se retrouvera à 9 h devant mon ancien appartement. La durée prévue est d’environ 3 à 4 heures. Les tâches à réaliser seront les suivantes : porter les cartons, démonter/porter les meubles, protéger les objets fragiles, puis aider à la mise en place dans le nouvel appartement. 
Pour vous remercier, je vous invite à dîner dans votre restaurant préféré après le déménagement. 
À bientôt, 
Haoyan`,
            answerCn: `亲爱的朋友们：
再次感谢你们愿意帮我搬家，搬家将在 5 月 5 日进行。我的新公寓在 1410，距离我原来的住所大约 20 分钟。
我们会在早上 9 点在我原来的公寓门口集合。预计总共需要大约 3 到 4 小时。需要完成的任务包括：搬箱子、拆卸/搬运家具、保护易碎物品，然后帮忙在新公寓里摆放安置。
为了感谢你们，搬家结束后我想请你们去你们最喜欢的餐厅吃晚饭。
回头见，
Haoyan`
          },
          {
            id: 17, topicCn: "10-06装修",
            promptFr: "Vous désirez changer l’aspect de votre logement (mobilier, couleurs, décorations, etc.). Vous écrivez à un(e) ami(e) pour partager votre projet et solliciter son assistance.",
            promptCn: "你想改变住处的整体风格/外观（家具、颜色、装饰等）。你给一位朋友写信/发消息，分享你的计划并请求他/她帮忙。",
            answerFr: `Cher Hao,
Je t’écris pour solliciter ton assistance. Je voudrais changer quelques meubles et décorations anciennes dans mon appartement. Je voudrais aussi repeindre plusieurs pièces comme les deux chambres, le salon et la cuisine. J’aimerais changer la couleur des murs.
D’abord, j’aurais besoin que tu me conseilles sur les marques de peintures, les outils à préparer et les couleurs à choisir. J’ai un budget de 2000 dollars. Ensuite, comme les travaux sont prévus de se dérouler la première semaine en juin, je souhaiterais que tu m’aides à repeindre les chambres.
Dis-moi ce que tu en penses.
À très bientôt,
Haoyan`,
            answerCn: `亲爱的 Luc：
我写信是想请你帮个忙。我想把公寓里一些旧家具和旧装饰换掉。我也想重新粉刷几间房间，比如两间卧室、客厅和厨房。我希望更换墙壁的颜色。
首先，我需要你给我一些建议：比如油漆品牌、需要准备的工具以及应该选择哪些颜色。我的预算是 2000 加元。其次，因为工程计划在 6 月的第一周进行，我希望你能帮我一起给卧室刷漆。
告诉我你的想法吧。
很快见，
Haoyan`
          },
          { type: "section", titleCn: "特殊类", descFr: "", descCn: "" },
          {
            id: 18, topicCn: "02-05卖自行车",
            promptFr: "« Je souhaite acheter un vélo fiable et pas cher. Merci de me contacter par mail : mathieu@gmail.com ». Vous possédez un vélo à vendre. Rédigez un courriel pour présenter votre vélo, fixer un prix et donner une date pour l’essayer.",
            promptCn: "“我想买一辆可靠又便宜的自行车。请通过邮箱联系我：mathieu@gmail.com。”你有一辆自行车要出售。请写一封邮件来介绍你的自行车、定一个价格，并给出一个可以试骑的日期。",
            answerFr: `Bonjour Mathieu,
J’espère que vous allez bien ! Je réponds à votre annonce pour l’achat d’un vélo.
Je vends un vélo de ville de marque Giant, couleur bleu foncé. Il est en bon état, presque neuf. Je l’ai utilisé pendant six mois. Je souhaiterais le laisser à 80 euros.
Je peux vous proposer un rendez-vous pour un essai ce samedi, devant la station de métro Yonge. Si vous êtes intéressé(e), n’hésitez pas à me contacter !
Cordialement,
Haoyan`,
            answerCn: `你好，Mathieu：
希望你一切都好！我写信是为了回复你购买自行车的那则公告。
我正在出售一辆 Giant（捷安特）品牌的城市自行车，深蓝色。车况很好，几乎是新的。我只使用了六个月。我希望以 80 欧元的价格出售。
我可以安排你本周六在 Yonge 地铁站门口试骑。如果你感兴趣，欢迎随时联系我！
此致敬礼，
Haoyan`
          },
          {
            id: 19, topicCn: "12-04传统节日",
            promptFr: "Votre ami Thomas vous écrit ce message : « Bonjour ! Je ne suis pas très familier avec la culture et les traditions de ton pays. Peux-tu me présenter une fête importante qui y est célébrée ? À bientôt ! » Rédigez une réponse dans laquelle vous décrivez une grande célébration de votre pays.",
            promptCn: "你的朋友 Thomas 给你写了这样一条消息： “你好！我对你国家的文化和传统不太熟悉。你能给我介绍一个在你们国家庆祝的重要节日吗？回头见！” 请写一封回复，在其中描述你国家的一项重要庆典/重大节日活动。",
            answerFr: `Cher Thomas,
Le Nouvel An chinois (Fête du Printemps), célébré fin janvier ou début février, est la fête la plus importante chez moi. Les familles se réunissent pour dîner, nettoient la maison, décorent en rouge et offrent des enveloppes rouges aux enfants. On regarde le gala, puis on assiste aux feux d’artifice et aux danses du lion. On mange des raviolis, du poisson et des gâteaux de riz, symboles de chance et de prospérité.
À bientôt,
Haoyan`,
            answerCn: `亲爱的 Thomas：
中国新年（春节）通常在一月底或二月初庆祝，是我家乡最重要的节日。家人会团聚吃年夜饭、打扫房子、用红色装饰，并给孩子们发红包。我们会看春节联欢晚会，然后欣赏烟花和舞狮表演。我们还会吃饺子、鱼和年糕，这些食物象征着好运与富足。
回头见，
Haoyan`
          },
          { type: "section", titleCn: "代管类", descFr: "", descCn: "" },
          {
            id: 20, topicCn: "11-09代管房子",
            promptFr: "« Salut ! Je suis prêt à veiller sur ta maison et ton jardin pendant tes vacances. Peux-tu me dire exactement ce que je dois faire ? À bientôt, Cédric » Rédigez un message à votre ami Cédric pour lui fournir des instructions concernant l’entretien de votre maison et de votre jardin pendant votre absence.",
            promptCn: "“嗨！我已经准备好在你度假期间帮你照看房子和花园了。你能告诉我我具体需要做什么吗？回头见，Cédric。”请给你的朋友 Cédric 写一条消息，向他提供你不在期间关于房屋和花园维护/照料的具体指示。",
            answerFr: `Cher Cédric,
Je t’écris afin de te donner des instructions pour que tu puisses mieux prendre soin de ma maison pendant mon absence. Je m’absenterai pour un voyage dès la semaine prochaine et je reviendrai au bout de trois semaines.
D’abord, je souhaiterais que tu passes chez moi au moins deux fois par semaine. Ensuite, j’aurais besoin que tu arroses les fleurs dans mon jardin chaque samedi. Enfin, il serait préférable de nettoyer la maison une fois par semaine.
J’écrirai les autres détails sur une feuille et je la déposerai sur la table, à côté des clés. En cas d’urgence, comme une fuite d’eau, appelle ma mère au 000-000-0000 : elle pourra t’aider.
Merci d’avance.
Haoyan`,
            answerCn: `亲爱的 Cédric：
我写信是想给你一些说明，好让你在我不在的时候能更好地照看我的房子。我从下周开始要去旅行，会离开三周，三周后回来。
首先，我希望你每周至少来我家两次。其次，我需要你每个星期六给花园里的花浇水。最后，最好每周把房子打扫一次。
其他细节我会写在一张纸上，并把它放在桌子上、钥匙旁边。如果遇到紧急情况，比如漏水，请拨打 000-000-0000 联系我妈妈：她可以帮助你。
提前谢谢你。
Haoyan`
          },
          {
            id: 21, topicCn: "03-05网购投诉",
            promptFr: "Rédiger un e-mail au service client pour signaler la réception d’un objet endommagé après une commande en ligne, en décrivant le problème et en précisant la solution souhaitée",
            promptCn: "给客服写一封电子邮件，说明你在网上下单后收到了损坏的商品，描述问题，并明确你希望的解决方案。",
            answerFr: `À l’attention du service client,
Je vous contacte à la suite de problèmes rencontrés lors de mon dernier achat sur votre site web, le 30 mai.
Je suis profondément déçu par le service fourni, notamment concernant le point suivant : à l’ouverture du colis, l’un des articles en porcelaine commandés était cassé, comme en attestent les photos jointes à ce message.
En conséquence, je demande un remboursement partiel des frais engagés, selon votre procédure, et vous remercie de bien vouloir traiter ma demande dans les plus brefs délais.
Je reste à votre disposition pour tout complément d’information.
Meilleures salutations,
Haoyan`,
            answerCn: `致客户服务部：
我联系您，是因为我于 5 月 30 日在贵网站进行的最近一次购买出现了问题。
我对所提供的服务感到非常失望，尤其是以下情况：打开包裹时，我订购的一件瓷器商品已经破损，随信附上的照片可以证明这一点。
因此，我希望按照贵方流程获得部分退款，并感谢贵方尽快处理我的请求。
如需任何补充信息，我愿随时提供。
此致敬礼，
Haoyan`
          },
          ]

"""

# ---- Config ----
TACHE = 1             # change to 2/3 if you want
KIND = "a"               # "a" for answers; if you insist, change to "q"
OUT_CSV = Path("assets/tcfEE/t1.csv")
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
