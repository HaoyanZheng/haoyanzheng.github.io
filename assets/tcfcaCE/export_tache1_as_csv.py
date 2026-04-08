#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
[
          { type: "section", titleCn: "T1", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Faire la preuve de son désir de travailler`, answerCn: `证明自己有工作的意愿` },
          { id: 2, topicCn: "", answerFr: `Leur nom s'est transformé en label de prestige`, answerCn: `他们的名字已经变成一种声望的标志` },
          { id: 3, topicCn: "", answerFr: `Des adaptations télévisées de Maupassant`, answerCn: `莫泊桑作品的电视改编` },
          { id: 4, topicCn: "", answerFr: `Entreprendre une rénovation du lieu`, answerCn: `着手对该地点进行翻修` },
          { id: 5, topicCn: "", answerFr: `C'est une réponse à des besoins alimentaires accrus`, answerCn: `这是对日益增长的食品需求的回应` },
          { id: 6, topicCn: "", answerFr: `Les producteurs évitent de prendre des risques`, answerCn: `生产者避免承担风险` },
          { id: 7, topicCn: "", answerFr: `Pour rester maître de sa vie privée`, answerCn: `为了保持对自己私人生活的掌控` },
          { id: 8, topicCn: "", answerFr: `Une diminution de la diversité de la faune océanique`, answerCn: `海洋动物多样性的减少` },
          { id: 9, topicCn: "", answerFr: `Gagner de l'argent pour payer leur séjour`, answerCn: `赚钱来支付他们的停留费用` },
          { id: 10, topicCn: "", answerFr: `Ils paraissent manipulés par une force supérieure`, answerCn: `他们似乎被一种更高的力量操控` },

          { type: "section", titleCn: "T2", descFr: "", descCn: "" },
          { id: 11, topicCn: "", answerFr: `De lutter contre les imitations`, answerCn: `与仿制品作斗争` },
          { id: 12, topicCn: "", answerFr: `Imite à la perfection la voix d'un enfant`, answerCn: `完美模仿孩子的声音` },
          { id: 13, topicCn: "", answerFr: `Son succès auprès des étudiants se dégrade`, answerCn: `他在学生中的受欢迎程度下降` },
          { id: 14, topicCn: "", answerFr: `Dormir efficacement`, answerCn: `高效睡眠` },
          { id: 15, topicCn: "", answerFr: `A financer les travaux du château par un don`, answerCn: `通过捐赠资助城堡修缮` },
          { id: 16, topicCn: "", answerFr: `La diversité des portraits présentés`, answerCn: `所展示肖像的多样性` },
          { id: 17, topicCn: "", answerFr: `Les gens en mangent plus que par le passé`, answerCn: `人们吃得比过去更多` },
          { id: 18, topicCn: "", answerFr: `Pour faire naître l'envie de s'investir dans un métier`, answerCn: `激发人们投身某职业的愿望` },
          { id: 19, topicCn: "", answerFr: `L'impartialité doit être l'une des qualités principales d'un maître`, answerCn: `公正必须是教师的主要品质之一` },
          { id: 20, topicCn: "", answerFr: `Pour dissimuler la pauvreté des contenus`, answerCn: `为了掩盖内容的贫乏` },

          { type: "section", titleCn: "T3", descFr: "", descCn: "" },
          { id: 21, topicCn: "", answerFr: `Envoyer des vœux de nouvel an`, answerCn: `发送新年祝福` },
          { id: 22, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众意见` },
          { id: 23, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可以被用作控制工具` },
          { id: 24, topicCn: "", answerFr: `Le triomphe d'une opinion émise par Apollinaire mais autrefois combattue`, answerCn: `阿波利奈尔提出但曾被反对的观点获得胜利` },
          { id: 25, topicCn: "", answerFr: `La fréquence de ses congénères`, answerCn: `其同类出现的频率` },
          { id: 26, topicCn: "", answerFr: `Elle aura un meilleur pouvoir d'achat sous peu`, answerCn: `她很快会拥有更强的购买力` },
          { id: 27, topicCn: "", answerFr: `Les ressources en gaz à l'échelle mondiale s'accroissent`, answerCn: `全球天然气资源正在增加` },
          { id: 28, topicCn: "", answerFr: `Une diminution de la diversité de la faune océanique.`, answerCn: `海洋动物多样性的减少。` },
          { id: 29, topicCn: "", answerFr: `La manipulation des clients par les industriels.`, answerCn: `工业企业对顾客的操控。` },
          { id: 30, topicCn: "", answerFr: `Aux hôtes du parlement.`, answerCn: `给议会的接待人员。` },

          { type: "section", titleCn: "T4", descFr: "", descCn: "" },
          { id: 31, topicCn: "", answerFr: `Démarrer une activité professionnelle`, answerCn: `开始一项职业活动` },
          { id: 32, topicCn: "", answerFr: `Faire rêver les petits patients`, answerCn: `让小患者充满梦想` },
          { id: 33, topicCn: "", answerFr: `Elle s'adresse exclusivement à une clientèle soucieuse des questions d'environnement`, answerCn: `它专门面向关注环保问题的顾客` },
          { id: 34, topicCn: "", answerFr: `Faire prendre conscience des excès liés à leur usage`, answerCn: `让人意识到使用过度的问题` },
          { id: 35, topicCn: "", answerFr: `D'aménager des réserves restreignant la pêche`, answerCn: `建立限制捕鱼的保护区` },
          { id: 36, topicCn: "", answerFr: `Les professeurs avec des compétences nécessaires sont rares`, answerCn: `具备必要能力的教师很少` },
          { id: 37, topicCn: "", answerFr: `Intégrer des valeurs sociales et environnementales`, answerCn: `融入社会和环境价值` },
          { id: 38, topicCn: "", answerFr: `Le film tombe dans les stéréotypes du genre`, answerCn: `电影落入类型刻板印象` },
          { id: 39, topicCn: "", answerFr: `L'impartialité doit être l'une des qualités principales d'un maître`, answerCn: `公正必须是教师的重要品质之一` },
          { id: 40, topicCn: "", answerFr: `Mettre en commun les données`, answerCn: `共享数据` },

          { type: "section", titleCn: "T5", descFr: "", descCn: "" },
          { id: 41, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在自己的奶酪里发现了某样东西` },
          { id: 42, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人建立联系` },
          { id: 43, topicCn: "", answerFr: `Pour participer à la finale d'un jeu`, answerCn: `为了参加一场比赛的决赛` },
          { id: 44, topicCn: "", answerFr: `Dormir efficacement`, answerCn: `高效睡眠` },
          { id: 45, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 46, topicCn: "", answerFr: `Il a cherché à préserver la beauté du site`, answerCn: `他试图保护这个地方的美丽` },
          { id: 47, topicCn: "", answerFr: `Ils développent leur culture du goût`, answerCn: `他们培养自己的味觉文化` },
          { id: 48, topicCn: "", answerFr: `Le gaspillage de l'eau dans le réseau domestique`, answerCn: `家庭供水系统中的水资源浪费` },
          { id: 49, topicCn: "", answerFr: `L'absence de programme politique`, answerCn: `缺乏政治纲领` },
          { id: 50, topicCn: "", answerFr: `Elles croyaient voir là leurs propres peintures`, answerCn: `她们以为在那里看到了自己的画` },

          { type: "section", titleCn: "T6", descFr: "", descCn: "" },
          { id: 51, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退还他的商品` },
          { id: 52, topicCn: "", answerFr: `C'est possible mais pénible`, answerCn: `这是可能的但很困难` },
          { id: 53, topicCn: "", answerFr: `Montrer l'importance de la chimie dans les rapports humains`, answerCn: `展示化学在人际关系中的重要性` },
          { id: 54, topicCn: "", answerFr: `Il estime qu'il reste du travail à faire pour mieux préparer cette évolution`, answerCn: `他认为仍需努力以更好准备这一变化` },
          { id: 55, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `由于互联网它可被越来越多用户使用` },
          { id: 56, topicCn: "", answerFr: `Le jeu des interprètes`, answerCn: `演员的表演` },
          { id: 57, topicCn: "", answerFr: `Elle entraîne un gain financier`, answerCn: `它带来经济收益` },
          { id: 58, topicCn: "", answerFr: `Pour faire naître l'envie de s'investir dans un métier`, answerCn: `激发人们投身某职业的愿望` },
          { id: 59, topicCn: "", answerFr: `Il transforme notre rapport au savoir`, answerCn: `它改变我们与知识的关系` },
          { id: 60, topicCn: "", answerFr: `L'ambiguïté du néologisme « chat » à l'écrit`, answerCn: `书面语中"chat"这一新词的歧义` },

          { type: "section", titleCn: "T7", descFr: "", descCn: "" },
          { id: 61, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人建立联系` },
          { id: 62, topicCn: "", answerFr: `Qui ont de l'expérience dans la télévente`, answerCn: `拥有电话销售经验的人` },
          { id: 63, topicCn: "", answerFr: `Du fait de sa taille`, answerCn: `由于它的规模` },
          { id: 64, topicCn: "", answerFr: `Le changement est définitif`, answerCn: `这种改变是永久的` },
          { id: 65, topicCn: "", answerFr: `Les produits utilisés dans les cultures`, answerCn: `农业中使用的产品` },
          { id: 66, topicCn: "", answerFr: `En envoyant des courriels sur la plateforme de l'émission`, answerCn: `通过在节目平台发送电子邮件` },
          { id: 67, topicCn: "", answerFr: `L'image attachée à sa profession est stéréotypée et peu valorisante`, answerCn: `与该职业相关的形象刻板且贬低` },
          { id: 68, topicCn: "", answerFr: `D'un catalogue de styliste`, answerCn: `来自一位时装设计师的目录` },
          { id: 69, topicCn: "", answerFr: `Son exploitation génère des revenus élevés`, answerCn: `其运营带来高额收入` },
          { id: 70, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },

          { type: "section", titleCn: "T8", descFr: "", descCn: "" },
          { id: 71, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 72, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 73, topicCn: "", answerFr: `Le besoin d'interaction sociale`, answerCn: `社交互动的需求` },
          { id: 74, topicCn: "", answerFr: `Elle trouve l'ensemble très réussi`, answerCn: `她认为整体非常成功` },
          { id: 75, topicCn: "", answerFr: `L'originalité des plats`, answerCn: `菜肴的独特性` },
          { id: 76, topicCn: "", answerFr: `Les professeurs avec des compétences nécessaires sont rares`, answerCn: `具备必要能力的教师很少` },
          { id: 77, topicCn: "", answerFr: `Faire la promotion de l'apprentissage d'un métier auprès des jeunes`, answerCn: `向年轻人推广职业培训` },
          { id: 78, topicCn: "", answerFr: `Elle modifie le rapport au temps`, answerCn: `它改变人们对时间的关系` },
          { id: 79, topicCn: "", answerFr: `La générosité qu'elle manifestait dans sa vie`, answerCn: `她在生活中表现出的慷慨` },
          { id: 80, topicCn: "", answerFr: `Il déclare que la photographie était une part nécessaire, mais non essentielle à son travail`, answerCn: `他表示摄影是其工作必要但非核心部分` },

          { type: "section", titleCn: "T9", descFr: "", descCn: "" },
          { id: 81, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 82, topicCn: "", answerFr: `Faire part de la réponse d'un responsable`, answerCn: `传达一位负责人给出的答复` },
          { id: 83, topicCn: "", answerFr: `Il risque d'entraver la circulation des véhicules de secours`, answerCn: `它可能阻碍救援车辆通行` },
          { id: 84, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可被用作控制工具` },
          { id: 85, topicCn: "", answerFr: `Elle masque les problèmes pédagogiques essentiels`, answerCn: `它掩盖了关键教学问题` },
          { id: 86, topicCn: "", answerFr: `Faire la promotion de l'apprentissage d'un métier auprès des jeunes`, answerCn: `向年轻人推广职业培训` },
          { id: 87, topicCn: "", answerFr: `Les gens en mangent plus que par le passé`, answerCn: `人们吃得比过去更多` },
          { id: 88, topicCn: "", answerFr: `D'un catalogue de styliste`, answerCn: `来自一位时装设计师的目录` },
          { id: 89, topicCn: "", answerFr: `La manipulation des clients par les industriels`, answerCn: `工业企业对消费者的操控` },
          { id: 90, topicCn: "", answerFr: `Le renoncement au nucléaire doit être mûrement planifié`, answerCn: `放弃核能必须慎重规划` },

          { type: "section", titleCn: "T10", descFr: "", descCn: "" },
          { id: 91, topicCn: "", answerFr: `En achetant les billets à l'avance`, answerCn: `通过提前购票` },
          { id: 92, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众意见` },
          { id: 93, topicCn: "", answerFr: `Le besoin d'interaction sociale`, answerCn: `社交互动的需求` },
          { id: 94, topicCn: "", answerFr: `De faire un bilan de leurs aptitudes`, answerCn: `评估他们的能力` },
          { id: 95, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `由于互联网越来越多用户可以使用` },
          { id: 96, topicCn: "", answerFr: `Le désir d'évolution durant la vie active`, answerCn: `职业生涯中的发展愿望` },
          { id: 97, topicCn: "", answerFr: `Ils se rendent régulièrement en ville`, answerCn: `他们经常进城` },
          { id: 98, topicCn: "", answerFr: `Elle modifie le rapport au temps`, answerCn: `它改变人们对时间的关系` },
          { id: 99, topicCn: "", answerFr: `La générosité qu'elle manifestait dans sa vie`, answerCn: `她在生活中表现出的慷慨` },
          { id: 100, topicCn: "", answerFr: `À favoriser l'émergence de valeurs culturelles collectives`, answerCn: `促进集体文化价值的形成` },

          { type: "section", titleCn: "T11", descFr: "", descCn: "" },
          { id: 101, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在自己的奶酪里发现了某样东西` },
          { id: 102, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 103, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃了很多` },
          { id: 104, topicCn: "", answerFr: `Des rendements en baisse`, answerCn: `产量下降` },
          { id: 105, topicCn: "", answerFr: `Mieux communiquer sur l'utilisation des fonds`, answerCn: `更好地说明资金的使用情况` },
          { id: 106, topicCn: "", answerFr: `En envoyant des courriels sur la plateforme de l'émission`, answerCn: `通过在节目平台发送电子邮件` },
          { id: 107, topicCn: "", answerFr: `L'image attachée à sa profession est stéréotypée et peu valorisante`, answerCn: `与该职业相关的形象刻板且不受重视` },
          { id: 108, topicCn: "", answerFr: `Obtenir de l'argent pour développer des centres d'accueil`, answerCn: `获得资金以发展接待中心` },
          { id: 109, topicCn: "", answerFr: `L'harmonisation de leurs appellations`, answerCn: `统一它们的名称` },
          { id: 110, topicCn: "", answerFr: `Il constate la fréquence des modifications apportées aux photos`, answerCn: `他注意到照片修改的频率` },

          { type: "section", titleCn: "T12", descFr: "", descCn: "" },
          { id: 111, topicCn: "", answerFr: `Responsabiliser les acteurs concernés`, answerCn: `让相关人员承担责任` },
          { id: 112, topicCn: "", answerFr: `Accueillir des artistes ainsi que leurs œuvres`, answerCn: `接待艺术家及其作品` },
          { id: 113, topicCn: "", answerFr: `L'homme se laisse dominer par la technologie`, answerCn: `人类被技术所支配` },
          { id: 114, topicCn: "", answerFr: `Le retard pris dans ses recherches`, answerCn: `研究中的延误` },
          { id: 115, topicCn: "", answerFr: `Il a écrit une œuvre abondante et variée`, answerCn: `他写了大量且多样的作品` },
          { id: 116, topicCn: "", answerFr: `Le sport sans douleur`, answerCn: `无痛运动` },
          { id: 117, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 118, topicCn: "", answerFr: `Ils alternent les supports selon le type d'activité`, answerCn: `他们根据活动类型更换媒介` },
          { id: 119, topicCn: "", answerFr: `À Paris et partout en Europe`, answerCn: `在巴黎以及整个欧洲` },
          { id: 120, topicCn: "", answerFr: `Que son dossier est examiné`, answerCn: `他的申请材料正在被审查` },

          { type: "section", titleCn: "T13", descFr: "", descCn: "" },
          { id: 121, topicCn: "", answerFr: `Son humour fait passer un message sérieux`, answerCn: `他的幽默传达了严肃的信息` },
          { id: 122, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人建立联系` },
          { id: 123, topicCn: "", answerFr: `Des adaptations télévisées de Maupassant`, answerCn: `莫泊桑作品的电视改编` },
          { id: 124, topicCn: "", answerFr: `L'expansion de la concurrence internationale`, answerCn: `国际竞争的扩大` },
          { id: 125, topicCn: "", answerFr: `Ils sont plus sûrs de leur nouveau choix`, answerCn: `他们对新的选择更加确定` },
          { id: 126, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 127, topicCn: "", answerFr: `Une mise en valeur de l'autre`, answerCn: `突出他人的价值` },
          { id: 128, topicCn: "", answerFr: `De simples citoyens`, answerCn: `普通公民` },
          { id: 129, topicCn: "", answerFr: `De la situation économique tendue`, answerCn: `紧张的经济形势` },
          { id: 130, topicCn: "", answerFr: `Les recherches sont limitées par le manque d'informations`, answerCn: `研究因信息不足而受限` },

          { type: "section", titleCn: "T14", descFr: "", descCn: "" },
          { id: 131, topicCn: "", answerFr: `La technologie modifie la relation à la gastronomie`, answerCn: `技术改变人与美食的关系` },
          { id: 132, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退还他的商品` },
          { id: 133, topicCn: "", answerFr: `C'est possible mais pénible`, answerCn: `这是可能但困难的` },
          { id: 134, topicCn: "", answerFr: `Il estime qu'il reste du travail à faire pour mieux préparer cette évolution`, answerCn: `他认为仍需努力以更好准备这一变化` },
          { id: 135, topicCn: "", answerFr: `D'aménager des réserves restreignant la pêche`, answerCn: `建立限制捕鱼的保护区` },
          { id: 136, topicCn: "", answerFr: `Ils permettent au système de se maintenir`, answerCn: `它们使系统得以维持` },
          { id: 137, topicCn: "", answerFr: `Ils alternent les supports selon le type d'activité`, answerCn: `他们根据活动类型更换媒介` },
          { id: 138, topicCn: "", answerFr: `D'un catalogue de styliste`, answerCn: `来自时装设计师的目录` },
          { id: 139, topicCn: "", answerFr: `Son exploitation génère des revenus élevés`, answerCn: `其运营带来高额收入` },
          { id: 140, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `农业耕作方法` },

          { type: "section", titleCn: "T15", descFr: "", descCn: "" },
          { id: 141, topicCn: "", answerFr: `L'expression du temps est opposée à la représentation habituelle`, answerCn: `时间表达方式与传统观念相反` },
          { id: 142, topicCn: "", answerFr: `Leur nom s'est transformé en label de prestige`, answerCn: `他们的名字变成一种声望标志` },
          { id: 143, topicCn: "", answerFr: `Pour participer à la finale d'un jeu`, answerCn: `为了参加比赛决赛` },
          { id: 144, topicCn: "", answerFr: `De lutter contre la saleté dans la capitale`, answerCn: `与首都的脏乱作斗争` },
          { id: 145, topicCn: "", answerFr: `Ils sont financés discrètement par des entreprises`, answerCn: `他们被企业秘密资助` },
          { id: 146, topicCn: "", answerFr: `Intégrer des valeurs sociales et environnementales`, answerCn: `融入社会和环境价值` },
          { id: 147, topicCn: "", answerFr: `Généraliser l'agriculture biologique`, answerCn: `推广有机农业` },
          { id: 148, topicCn: "", answerFr: `Une diminution de la diversité de la faune océanique`, answerCn: `海洋动物多样性的减少` },
          { id: 149, topicCn: "", answerFr: `Une manifestation culturelle`, answerCn: `文化活动` },
          { id: 150, topicCn: "", answerFr: `Pour dissimuler la pauvreté des contenus`, answerCn: `为了掩盖内容贫乏` },

          { type: "section", titleCn: "T16", descFr: "", descCn: "" },
          { id: 151, topicCn: "", answerFr: `Favoriser la mobilité urbaine grâce aux cycles non motorisés.`, answerCn: `借助非机动自行车促进城市出行` },
          { id: 152, topicCn: "", answerFr: `Il a trouvé les causes du rétrécissement de la laine`, answerCn: `他找到了羊毛缩水的原因` },
          { id: 153, topicCn: "", answerFr: `Elle a diversifié son alimentation`, answerCn: `她使自己的饮食更加多样化` },
          { id: 154, topicCn: "", answerFr: `Son succès auprès des étudiants se dégrade`, answerCn: `他在学生中的受欢迎程度下降` },
          { id: 155, topicCn: "", answerFr: `Le personnel manque de chaleur et d'amabilité`, answerCn: `工作人员缺乏热情和友好` },
          { id: 156, topicCn: "", answerFr: `Ils sont financés discrètement par des entreprises`, answerCn: `他们被企业秘密资助` },
          { id: 157, topicCn: "", answerFr: `Du manque de familles d'accueil`, answerCn: `由于寄宿家庭不足` },
          { id: 158, topicCn: "", answerFr: `La réelle dimension écologique du festival`, answerCn: `这个节日真正的生态意义` },
          { id: 159, topicCn: "", answerFr: `Le message véhiculé par la publicité était inacceptable`, answerCn: `广告传递的信息是不可接受的` },
          { id: 160, topicCn: "", answerFr: `Ce sont les violons récents qui sont les plus estimés`, answerCn: `最近制作的小提琴最受重视` },

          { type: "section", titleCn: "T17", descFr: "", descCn: "" },
          { id: 161, topicCn: "", answerFr: `Une perte de spontanéité des matchs`, answerCn: `比赛失去了自发性` },
          { id: 162, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 163, topicCn: "", answerFr: `Il nécessite une réorganisation des lieux les plus visités`, answerCn: `这需要重新组织最常访问的地方` },
          { id: 164, topicCn: "", answerFr: `C'est un carrefour culturel intercontinental`, answerCn: `这是一个跨洲文化交汇点` },
          { id: 165, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `由于互联网越来越多用户可以访问` },
          { id: 166, topicCn: "", answerFr: `Pour obtenir des données sur sa composition`, answerCn: `为了获得其成分数据` },
          { id: 167, topicCn: "", answerFr: `De nouvelles pédagogies semblent nécessaires`, answerCn: `新的教学方法似乎是必要的` },
          { id: 168, topicCn: "", answerFr: `Les doutes sur les méthodes de production`, answerCn: `对生产方法的怀疑` },
          { id: 169, topicCn: "", answerFr: `La manipulation des clients par les industriels`, answerCn: `工业企业对顾客的操控` },
          { id: 170, topicCn: "", answerFr: `Faire évoluer les mentalités au sujet du handicap au travail`, answerCn: `改变人们对职场残疾问题的观念` },

          { type: "section", titleCn: "T18", descFr: "", descCn: "" },
          { id: 171, topicCn: "", answerFr: `Son humour fait passer un message sérieux`, answerCn: `他的幽默传达严肃信息` },
          { id: 172, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人建立联系` },
          { id: 173, topicCn: "", answerFr: `Elle masque les problèmes pédagogiques essentiels`, answerCn: `它掩盖了关键的教学问题` },
          { id: 174, topicCn: "", answerFr: `Entreprendre une rénovation du lieu`, answerCn: `着手翻修这个地方` },
          { id: 175, topicCn: "", answerFr: `Très peu de francophones occupent des fonctions à responsabilité`, answerCn: `很少有法语人士担任管理职位` },
          { id: 176, topicCn: "", answerFr: `S'ils appartiennent à une espèce adéquate`, answerCn: `如果它们属于合适的物种` },
          { id: 177, topicCn: "", answerFr: `Généraliser l'agriculture biologique`, answerCn: `推广有机农业` },
          { id: 178, topicCn: "", answerFr: `Diminuer les risques sanitaires`, answerCn: `减少健康风险` },
          { id: 179, topicCn: "", answerFr: `Le développement d'une conscience civique`, answerCn: `公民意识的发展` },
          { id: 180, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `农业耕作方法` },

          { type: "section", titleCn: "T19", descFr: "", descCn: "" },
          { id: 181, topicCn: "", answerFr: `Présenter les relations familiales avec humour`, answerCn: `用幽默方式展现家庭关系` },
          { id: 182, topicCn: "", answerFr: `Une activité de maquillage`, answerCn: `化妆活动` },
          { id: 183, topicCn: "", answerFr: `De signaler sur les photos les modifications effectuées`, answerCn: `标注照片中所做的修改` },
          { id: 184, topicCn: "", answerFr: `Le confort a été très nettement amélioré`, answerCn: `舒适度明显提高` },
          { id: 185, topicCn: "", answerFr: `De nouvelles pratiques de vente`, answerCn: `新的销售方式` },
          { id: 186, topicCn: "", answerFr: `C'est une réclamation destinée au gérant d'un immeuble`, answerCn: `这是给楼房管理员的投诉` },
          { id: 187, topicCn: "", answerFr: `Intégrer des valeurs sociales et environnementales`, answerCn: `融入社会和环境价值` },
          { id: 188, topicCn: "", answerFr: `Empêcher le trafic des fromages de contrebande`, answerCn: `阻止奶酪走私交易` },
          { id: 189, topicCn: "", answerFr: `D'une pollution imperceptible`, answerCn: `一种难以察觉的污染` },
          { id: 190, topicCn: "", answerFr: `Ils paraissent manipulés par une force supérieure`, answerCn: `他们似乎被某种更高力量操控` },

          { type: "section", titleCn: "T20", descFr: "", descCn: "" },
          { id: 191, topicCn: "", answerFr: `Des séjours alliant détente et découvertes`, answerCn: `结合休闲与探索的旅行` },
          { id: 192, topicCn: "", answerFr: `Son ambiance créative`, answerCn: `其富有创意的氛围` },
          { id: 193, topicCn: "", answerFr: `Le confort a été très nettement amélioré`, answerCn: `舒适度明显提高` },
          { id: 194, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃得很多` },
          { id: 195, topicCn: "", answerFr: `À financer les travaux du château par un don`, answerCn: `通过捐赠资助城堡维修` },
          { id: 196, topicCn: "", answerFr: `Améliorer les relations au sein du lycée`, answerCn: `改善学校内部关系` },
          { id: 197, topicCn: "", answerFr: `Trouver des valeurs communes`, answerCn: `寻找共同价值` },
          { id: 198, topicCn: "", answerFr: `Il critique son concept`, answerCn: `他批评这一概念` },
          { id: 199, topicCn: "", answerFr: `Ils perpétuent une forme d'exclusion`, answerCn: `他们延续了一种排斥现象` },
          { id: 200, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `农业耕作方法` },

          { type: "section", titleCn: "T21", descFr: "", descCn: "" },
          { id: 201, topicCn: "", answerFr: `Il explique l'idée de départ d'un livre de Modiano`, answerCn: `他解释了莫迪亚诺一本书的创作起点` },
          { id: 202, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退还他的商品` },
          { id: 203, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `选择一段回忆` },
          { id: 204, topicCn: "", answerFr: `Elle entraîne une trop grande consommation d'énergie`, answerCn: `它导致过高的能源消耗` },
          { id: 205, topicCn: "", answerFr: `Ils sont financés discrètement par des entreprises`, answerCn: `他们被企业秘密资助` },
          { id: 206, topicCn: "", answerFr: `Par la primauté de l'intérêt collectif sur bénéfices`, answerCn: `以集体利益优先于利润为原则` },
          { id: 207, topicCn: "", answerFr: `L'image attachée à sa profession est stéréotypée et peu valorisante`, answerCn: `该职业的形象刻板且不被重视` },
          { id: 208, topicCn: "", answerFr: `Il envisage avec optimisme les futurs possibles`, answerCn: `他乐观地看待未来的可能性` },
          { id: 209, topicCn: "", answerFr: `À quel problème sont confrontés les distributeurs indépendants`, answerCn: `独立经销商面临什么问题` },
          { id: 210, topicCn: "", answerFr: `Travailler sur soi-même`, answerCn: `自我提升` },

          { type: "section", titleCn: "T22", descFr: "", descCn: "" },
          { id: 211, topicCn: "", answerFr: `Il explique l'idée de départ d'un livre de Modiano`, answerCn: `他解释莫迪亚诺一本书的创作起点` },
          { id: 212, topicCn: "", answerFr: `Une activité de maquillage`, answerCn: `化妆活动` },
          { id: 213, topicCn: "", answerFr: `Être amateur de viande et militer pour le bien-être animal`, answerCn: `既喜欢吃肉又倡导动物福利` },
          { id: 214, topicCn: "", answerFr: `Définir les conditions d'accueil des élèves en milieu professionnel`, answerCn: `规定学生在工作环境中的接待条件` },
          { id: 215, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `由于互联网越来越多用户可以访问` },
          { id: 216, topicCn: "", answerFr: `Pour obtenir des données sur sa composition`, answerCn: `为了获取其成分数据` },
          { id: 217, topicCn: "", answerFr: `L'essor de nouveaux modes de consommation`, answerCn: `新消费方式的兴起` },
          { id: 218, topicCn: "", answerFr: `Organiser des séjours à vocation humanitaire`, answerCn: `组织人道主义旅行` },
          { id: 219, topicCn: "", answerFr: `Il est difficile d'en évaluer l'impact sur la santé`, answerCn: `很难评估它对健康的影响` },
          { id: 220, topicCn: "", answerFr: `Pour dissimuler la pauvreté des contenus`, answerCn: `为了掩盖内容的贫乏` },

          { type: "section", titleCn: "T23", descFr: "", descCn: "" },
          { id: 221, topicCn: "", answerFr: `Leur nom s'est transformé en label de prestige`, answerCn: `他们的名字已经成为一种声望标志` },
          { id: 222, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退还商品` },
          { id: 223, topicCn: "", answerFr: `D'analyser les moyens de séduire les jeunes`, answerCn: `分析吸引年轻人的方法` },
          { id: 224, topicCn: "", answerFr: `Elle permet de dépenser moins d'argent`, answerCn: `它可以减少花费` },
          { id: 225, topicCn: "", answerFr: `L'originalité des plats`, answerCn: `菜肴的独特性` },
          { id: 226, topicCn: "", answerFr: `Un rappel d'un impayé en cours`, answerCn: `提醒尚未支付的账款` },
          { id: 227, topicCn: "", answerFr: `Elle répond de manière pertinente aux difficultés et aux aspirations des élèves`, answerCn: `它很好地回应学生的困难与愿望` },
          { id: 228, topicCn: "", answerFr: `Obtenir de l'argent pour développer des centres d'accueil`, answerCn: `获得资金发展接待中心` },
          { id: 229, topicCn: "", answerFr: `Des outils de communication`, answerCn: `沟通工具` },
          { id: 230, topicCn: "", answerFr: `L'ambiguïté du néologisme « chat » à l'écrit`, answerCn: `书面语中"chat"这一新词的歧义` },

          { type: "section", titleCn: "T24", descFr: "", descCn: "" },
          { id: 231, topicCn: "", answerFr: `La technologie modifie la relation à la gastronomie`, answerCn: `技术改变人与美食的关系` },
          { id: 232, topicCn: "", answerFr: `Pour créer un lien entre générations`, answerCn: `为了在不同世代之间建立联系` },
          { id: 233, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `选择一段回忆` },
          { id: 234, topicCn: "", answerFr: `Il a acclamé de toutes ses forces la chanteuse`, answerCn: `他竭尽全力为歌手欢呼` },
          { id: 235, topicCn: "", answerFr: `D'aménager des réserves restreignant la pêche`, answerCn: `建立限制捕鱼的保护区` },
          { id: 236, topicCn: "", answerFr: `De vérifier le profil des postulants`, answerCn: `核查申请者的背景` },
          { id: 237, topicCn: "", answerFr: `Une mise en valeur de l'autre`, answerCn: `突出他人的价值` },
          { id: 238, topicCn: "", answerFr: `Elle modifie le rapport au temps`, answerCn: `它改变人们对时间的关系` },
          { id: 239, topicCn: "", answerFr: `Transmettre des connaissances`, answerCn: `传递知识` },
          { id: 240, topicCn: "", answerFr: `Que ses écrits permettent de mieux cerner qu'il était`, answerCn: `他的作品帮助更好了解他是谁` },

          { type: "section", titleCn: "T25", descFr: "", descCn: "" },
          { id: 241, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 242, topicCn: "", answerFr: `Le public se reconnaît à travers les héros`, answerCn: `观众在英雄人物中看到自己` },
          { id: 243, topicCn: "", answerFr: `À une simulation de mission spatiale`, answerCn: `一次模拟太空任务` },
          { id: 244, topicCn: "", answerFr: `Être titulaire d'une formation reconnue`, answerCn: `拥有认可的培训资格` },
          { id: 245, topicCn: "", answerFr: `Favoriser l'égalité des chances`, answerCn: `促进机会平等` },
          { id: 246, topicCn: "", answerFr: `L'optimisation de leur gestion est en cours d'étude`, answerCn: `正在研究如何优化其管理` },
          { id: 247, topicCn: "", answerFr: `Les producteurs évitent de prendre des risques`, answerCn: `生产者避免承担风险` },
          { id: 248, topicCn: "", answerFr: `Elle abrite une vie animée`, answerCn: `那里生活非常活跃` },
          { id: 249, topicCn: "", answerFr: `Choisir des actions pour leur commune`, answerCn: `为他们的社区选择行动方案` },
          { id: 250, topicCn: "", answerFr: `Il appartient à une réflexion philosophique`, answerCn: `它属于哲学思考的一部分` },

          { type: "section", titleCn: "T26", descFr: "", descCn: "" },
          { id: 251, topicCn: "", answerFr: `Il explique l'idée de départ d'un livre de Modiano`, answerCn: `他解释莫迪亚诺一本书的创作起点` },
          { id: 252, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众意见` },
          { id: 253, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可以被用作控制工具` },
          { id: 254, topicCn: "", answerFr: `De faire un bilan de leurs aptitudes`, answerCn: `评估他们的能力` },
          { id: 255, topicCn: "", answerFr: `Ils intègrent l'ancien à leurs constructions`, answerCn: `他们在建筑中融合旧元素` },
          { id: 256, topicCn: "", answerFr: `Les grandes surfaces provoquent la fin des petites boutiques de quartier`, answerCn: `大型商场导致社区小店消失` },
          { id: 257, topicCn: "", answerFr: `De la volonté d'émancipation`, answerCn: `一种解放自主的愿望` },
          { id: 258, topicCn: "", answerFr: `Il remet en question leurs retombées positives`, answerCn: `他质疑其积极影响` },
          { id: 259, topicCn: "", answerFr: `Le développement d'une conscience civique`, answerCn: `公民意识的发展` },
          { id: 260, topicCn: "", answerFr: `Faire évoluer les mentalités au sujet du handicap au travail`, answerCn: `改变人们对职场残疾问题的看法` },

          { type: "section", titleCn: "T27", descFr: "", descCn: "" },
          { id: 261, topicCn: "", answerFr: `Elle récolte les produits de terrains privés`, answerCn: `她从私人土地采集产品` },
          { id: 262, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 263, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `选择一段回忆` },
          { id: 264, topicCn: "", answerFr: `Il a écrit une œuvre abondante et variée`, answerCn: `他写了大量且多样的作品` },
          { id: 265, topicCn: "", answerFr: `Elles contribuent à protéger l'environnement`, answerCn: `它们有助于保护环境` },
          { id: 266, topicCn: "", answerFr: `Il sera proche d'un jardin public`, answerCn: `它将靠近一个公共花园` },
          { id: 267, topicCn: "", answerFr: `Elle est modelée par ses locuteurs`, answerCn: `它由使用者塑造` },
          { id: 268, topicCn: "", answerFr: `Respecter les normes internationales`, answerCn: `遵守国际标准` },
          { id: 269, topicCn: "", answerFr: `Démontrer les dégâts des méthodes de culture intensive`, answerCn: `证明集约农业方法的危害` },
          { id: 270, topicCn: "", answerFr: `Elle est incompatible avec les objets politiques`, answerCn: `它与政治对象不兼容` },

          { type: "section", titleCn: "T28", descFr: "", descCn: "" },
          { id: 271, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在自己的奶酪里发现了某样东西` },
          { id: 272, topicCn: "", answerFr: `Actrice à la télévision française`, answerCn: `法国电视演员` },
          { id: 273, topicCn: "", answerFr: `Elle a diversifié son alimentation`, answerCn: `她让饮食更加多样化` },
          { id: 274, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `选择一段回忆` },
          { id: 275, topicCn: "", answerFr: `Le triomphe d'une opinion émise par Apollinaire mais autrefois combattue`, answerCn: `阿波利奈尔提出但曾被反对的观点获得胜利` },
          { id: 276, topicCn: "", answerFr: `De vérifier le profil des postulants`, answerCn: `核查申请者背景` },
          { id: 277, topicCn: "", answerFr: `Il remet en question leurs retombées positives`, answerCn: `他质疑其积极影响` },
          { id: 278, topicCn: "", answerFr: `La coopération de ses membres`, answerCn: `成员之间的合作` },
          { id: 279, topicCn: "", answerFr: `Elles représentent inégalement les milieux sociaux`, answerCn: `它们对不同社会阶层的代表性不均衡` },
          { id: 280, topicCn: "", answerFr: `Les recherches sont limitées par le manque d'informations`, answerCn: `研究因信息不足而受限` },

          { type: "section", titleCn: "T29", descFr: "", descCn: "" },
          { id: 281, topicCn: "", answerFr: `Elle récolte les produits de terrains privés`, answerCn: `她从私人土地采集产品` },
          { id: 282, topicCn: "", answerFr: `Imite à la perfection la voix d'un enfant`, answerCn: `完美模仿孩子的声音` },
          { id: 283, topicCn: "", answerFr: `Ils permettent de protéger la biodiversité`, answerCn: `它们有助于保护生物多样性` },
          { id: 284, topicCn: "", answerFr: `Il a écrit une œuvre abondante et variée`, answerCn: `他写了大量且多样的作品` },
          { id: 285, topicCn: "", answerFr: `Elles contribuent à protéger l'environnement`, answerCn: `它们有助于保护环境` },
          { id: 286, topicCn: "", answerFr: `En révisant les conditions de rémunération`, answerCn: `通过调整薪酬条件` },
          { id: 287, topicCn: "", answerFr: `Elle est modelée par ses locuteurs`, answerCn: `它由使用者塑造` },
          { id: 288, topicCn: "", answerFr: `Il critique son concept`, answerCn: `他批评这一概念` },
          { id: 289, topicCn: "", answerFr: `Transmettre des connaissances`, answerCn: `传递知识` },
          { id: 290, topicCn: "", answerFr: `Elles modifient nos processus cognitifs`, answerCn: `它们改变我们的认知过程` },

          { type: "section", titleCn: "T30", descFr: "", descCn: "" },
          { id: 291, topicCn: "", answerFr: `Elle peut perdre son statut de langue dominante`, answerCn: `它可能失去主导语言地位` },
          { id: 292, topicCn: "", answerFr: `Une perte de spontanéité des matchs`, answerCn: `比赛失去自发性` },
          { id: 293, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 294, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃了很多` },
          { id: 295, topicCn: "", answerFr: `La réforme des retraites influencera leurs comportements`, answerCn: `养老金改革将影响他们的行为` },
          { id: 296, topicCn: "", answerFr: `À une simulation de mission spatiale`, answerCn: `一次模拟太空任务` },
          { id: 297, topicCn: "", answerFr: `On ignore comment elles ont été réalisées`, answerCn: `人们不知道它们是如何完成的` },
          { id: 298, topicCn: "", answerFr: `Cela favorise l'intégration de nouvelles espèces et est bon pour l'écosystème`, answerCn: `这有利于新物种的融入并有益生态系统` },
          { id: 299, topicCn: "", answerFr: `Interpréter certains rôles`, answerCn: `扮演某些角色` },
          { id: 300, topicCn: "", answerFr: `Démontrer les dégâts des méthodes de culture intensive`, answerCn: `证明集约农业方法的危害` },

          { type: "section", titleCn: "T31", descFr: "", descCn: "" },
          { id: 301, topicCn: "", answerFr: `La technologie modifie la relation à la gastronomie`, answerCn: `技术改变人与美食的关系` },
          { id: 302, topicCn: "", answerFr: `L'adaptation de l'offre culinaire à la mode actuelle`, answerCn: `餐饮供应适应当前潮流` },
          { id: 303, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `选择一段回忆` },
          { id: 304, topicCn: "", answerFr: `Elle soutient l'esprit de création`, answerCn: `它支持创造精神` },
          { id: 305, topicCn: "", answerFr: `Ils sont plus sûrs de leur nouveau choix`, answerCn: `他们对新选择更加确定` },
          { id: 306, topicCn: "", answerFr: `Ils permettent au système de se maintenir`, answerCn: `它们使系统得以维持` },
          { id: 307, topicCn: "", answerFr: `De nouvelles pédagogies semblent nécessaires`, answerCn: `新的教学方式似乎是必要的` },
          { id: 308, topicCn: "", answerFr: `Le nombre d'ouvrages à paraître a diminué`, answerCn: `即将出版的书籍数量减少` },
          { id: 309, topicCn: "", answerFr: `Ils perpétuent une forme d'exclusion`, answerCn: `他们延续了一种排斥现象` },
          { id: 310, topicCn: "", answerFr: `Elles contribuent à une bonne hygiène de vie.`, answerCn: `它们有助于保持良好的生活习惯。` },

          { type: "section", titleCn: "T32", descFr: "", descCn: "" },
          { id: 311, topicCn: "", answerFr: `Elle récolte les produits de terrains privés`, answerCn: `她从私人土地采集产品` },
          { id: 312, topicCn: "", answerFr: `Avoir la garantie de la qualité du produit et ignorer d'où il vient`, answerCn: `保证产品质量但不知道来源` },
          { id: 313, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可以被用作控制工具` },
          { id: 314, topicCn: "", answerFr: `Elle associe différentes formes d'expression artistique`, answerCn: `它结合多种艺术表达形式` },
          { id: 315, topicCn: "", answerFr: `Il soutient les entreprises locales`, answerCn: `他支持本地企业` },
          { id: 316, topicCn: "", answerFr: `Pour soutenir les agriculteurs de proximité`, answerCn: `为了支持当地农民` },
          { id: 317, topicCn: "", answerFr: `Les ressources en gaz à l'échelle mondiale s'accroissent`, answerCn: `全球天然气资源正在增加` },
          { id: 318, topicCn: "", answerFr: `De l'organisation d'une animation clandestine`, answerCn: `组织秘密活动` },
          { id: 319, topicCn: "", answerFr: `Une manifestation culturelle`, answerCn: `文化活动` },
          { id: 320, topicCn: "", answerFr: `La mise en œuvre d'une action collective`, answerCn: `实施集体行动` },

          { type: "section", titleCn: "T33", descFr: "", descCn: "" },
          { id: 321, topicCn: "", answerFr: `En achetant les billets à l'avance`, answerCn: `通过提前购票` },
          { id: 322, topicCn: "", answerFr: `L'organisation d'un événement culturel`, answerCn: `组织一项文化活动` },
          { id: 323, topicCn: "", answerFr: `Il risque d'entraver la circulation des véhicules de secours`, answerCn: `它可能阻碍救援车辆通行` },
          { id: 324, topicCn: "", answerFr: `Pour proposer davantage de places`, answerCn: `为了提供更多座位` },
          { id: 325, topicCn: "", answerFr: `Ouvrir une bibliothèque pour tous`, answerCn: `为所有人开放图书馆` },
          { id: 326, topicCn: "", answerFr: `La diversité des portraits présentés`, answerCn: `展示肖像的多样性` },
          { id: 327, topicCn: "", answerFr: `Pour dénoncer le manque d'entretien`, answerCn: `为了谴责维护不足` },
          { id: 328, topicCn: "", answerFr: `Le film tombe dans les stéréotypes du genre`, answerCn: `电影落入类型刻板印象` },
          { id: 329, topicCn: "", answerFr: `Le recrutement de personnels qualifiés`, answerCn: `招聘合格人员` },
          { id: 330, topicCn: "", answerFr: `Demander à une cliente de payer l'intégralité de sa commande`, answerCn: `要求顾客支付全部订单金额` },

          { type: "section", titleCn: "T34", descFr: "", descCn: "" },
          { id: 331, topicCn: "", answerFr: `Un espace de remise en forme`, answerCn: `一个健身空间` },
          { id: 332, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 333, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `选择一段回忆` },
          { id: 334, topicCn: "", answerFr: `Il a acclamé de toutes ses forces la chanteuse`, answerCn: `他竭尽全力为歌手欢呼` },
          { id: 335, topicCn: "", answerFr: `Pour proposer davantage de places`, answerCn: `为了提供更多位置` },
          { id: 336, topicCn: "", answerFr: `Mieux communiquer sur l'utilisation des fonds`, answerCn: `更好说明资金使用情况` },
          { id: 337, topicCn: "", answerFr: `Trouver des valeurs communes`, answerCn: `寻找共同价值` },
          { id: 338, topicCn: "", answerFr: `Diversifier les activités en centre-ville`, answerCn: `使市中心活动多样化` },
          { id: 339, topicCn: "", answerFr: `De la situation économique tendue`, answerCn: `紧张的经济形势` },
          { id: 340, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },

          { type: "section", titleCn: "T35", descFr: "", descCn: "" },
          { id: 341, topicCn: "", answerFr: `L'adaptation de l'offre culinaire à la mode actuelle`, answerCn: `餐饮供应适应当前潮流` },
          { id: 342, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退还商品` },
          { id: 343, topicCn: "", answerFr: `Il influence la productivité des salariés`, answerCn: `它影响员工生产力` },
          { id: 344, topicCn: "", answerFr: `La multiplication des éclairages publics`, answerCn: `公共照明的增加` },
          { id: 345, topicCn: "", answerFr: `Il facilite la lecture des étiquettes`, answerCn: `它使标签更容易阅读` },
          { id: 346, topicCn: "", answerFr: `Ils incitent leur entourage à les imiter`, answerCn: `他们鼓励周围的人模仿` },
          { id: 347, topicCn: "", answerFr: `Elle répond aux tendances actuelles`, answerCn: `它符合当前趋势` },
          { id: 348, topicCn: "", answerFr: `Le nombre d'ouvrages à paraître a diminué`, answerCn: `即将出版的书籍数量减少` },
          { id: 349, topicCn: "", answerFr: `La mise en œuvre d'une action collective`, answerCn: `实施集体行动` },
          { id: 350, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `农业耕作方法` },

          { type: "section", titleCn: "T36", descFr: "", descCn: "" },
          { id: 351, topicCn: "", answerFr: `Pour créer un lien entre générations`, answerCn: `为了在不同世代之间建立联系` },
          { id: 352, topicCn: "", answerFr: `Une activité de maquillage`, answerCn: `化妆活动` },
          { id: 353, topicCn: "", answerFr: `De signaler sur les photos les modifications effectuées`, answerCn: `标注照片中的修改` },
          { id: 354, topicCn: "", answerFr: `Il influence la productivité des salariés`, answerCn: `它影响员工生产力` },
          { id: 355, topicCn: "", answerFr: `L'expansion de la concurrence internationale`, answerCn: `国际竞争的扩大` },
          { id: 356, topicCn: "", answerFr: `Il facilite la lecture des étiquettes`, answerCn: `它使标签更易阅读` },
          { id: 357, topicCn: "", answerFr: `Il se propage imperceptiblement`, answerCn: `它在不知不觉中传播` },
          { id: 358, topicCn: "", answerFr: `Décrire les rapports du sport et de la politique internationale`, answerCn: `描述体育与国际政治的关系` },
          { id: 359, topicCn: "", answerFr: `Travailler sur soi-même`, answerCn: `自我提升` },
          { id: 360, topicCn: "", answerFr: `Il est indissociable de celui des savoirs`, answerCn: `它与知识的发展不可分离` },

          { type: "section", titleCn: "T37", descFr: "", descCn: "" },
          { id: 361, topicCn: "", answerFr: `Créer un site collaboratif de données`, answerCn: `创建协作数据网站` },
          { id: 362, topicCn: "", answerFr: `Il modifie le moment du coucher`, answerCn: `它改变就寝时间` },
          { id: 363, topicCn: "", answerFr: `De limiter le gaspillage alimentaire`, answerCn: `限制食物浪费` },
          { id: 364, topicCn: "", answerFr: `Le besoin d'interaction sociale`, answerCn: `社交互动的需求` },
          { id: 365, topicCn: "", answerFr: `Aux étincelles produites par des perturbations orageuses`, answerCn: `由雷暴扰动产生的火花` },
          { id: 366, topicCn: "", answerFr: `Rebelle à toute forme d'autorité`, answerCn: `反抗一切权威形式` },
          { id: 367, topicCn: "", answerFr: `Le malentendu sur le lieu où est enterré Brassens`, answerCn: `关于布拉桑斯埋葬地点的误解` },
          { id: 368, topicCn: "", answerFr: `Les doutes sur les méthodes de production`, answerCn: `对生产方式的怀疑` },
          { id: 369, topicCn: "", answerFr: `Elles gagnent en visibilité dans ce milieu`, answerCn: `它们在这个领域越来越显眼` },
          { id: 370, topicCn: "", answerFr: `Elles modifient nos processus cognitifs`, answerCn: `它们改变我们的认知过程` },

          { type: "section", titleCn: "T38", descFr: "", descCn: "" },
          { id: 371, topicCn: "", answerFr: `Des séjours alliant détente et découvertes`, answerCn: `结合休闲与探索的旅行` },
          { id: 372, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众意见` },
          { id: 373, topicCn: "", answerFr: `C'est possible mais pénible`, answerCn: `这是可能但困难的` },
          { id: 374, topicCn: "", answerFr: `Pour donner une bonne image d'eux`, answerCn: `为了给人留下好印象` },
          { id: 375, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 376, topicCn: "", answerFr: `Il peut s'étendre au domaine personnel`, answerCn: `它可以扩展到个人领域` },
          { id: 377, topicCn: "", answerFr: `De la volonté d'émancipation`, answerCn: `一种解放自主的愿望` },
          { id: 378, topicCn: "", answerFr: `Le respect de la déontologie médicale est primordial`, answerCn: `遵守医学伦理至关重要` },
          { id: 379, topicCn: "", answerFr: `Des outils ont été élaborés pour en estimer l'intensité`, answerCn: `已开发工具来估计其强度` },
          { id: 380, topicCn: "", answerFr: `Il donne un conseil`, answerCn: `他提出一个建议` },

          { type: "section", titleCn: "T39", descFr: "", descCn: "" },
          { id: 381, topicCn: "", answerFr: `Le secret d'une bonne préparation`, answerCn: `良好准备的秘诀` },
          { id: 382, topicCn: "", answerFr: `Présenter les relations familiales avec humour`, answerCn: `用幽默方式展现家庭关系` },
          { id: 383, topicCn: "", answerFr: `C'est possible mais pénible`, answerCn: `这是可能但困难的` },
          { id: 384, topicCn: "", answerFr: `Pour donner une bonne image d'eux`, answerCn: `为了给人留下好印象` },
          { id: 385, topicCn: "", answerFr: `Parce que l'événement s'inscrit dans un principe d'universalité`, answerCn: `因为该活动遵循普遍性原则` },
          { id: 386, topicCn: "", answerFr: `Les produits utilisés dans les cultures`, answerCn: `农业中使用的产品` },
          { id: 387, topicCn: "", answerFr: `La bonne humeur garantit de meilleures performances`, answerCn: `好心情能带来更好表现` },
          { id: 388, topicCn: "", answerFr: `Le message véhiculé par la publicité était inacceptable`, answerCn: `广告传递的信息不可接受` },
          { id: 389, topicCn: "", answerFr: `Ils s'impliquent de façon responsable dans les cours`, answerCn: `他们在课程中负责任地参与` },
          { id: 390, topicCn: "", answerFr: `Comme une incitation à l'action.`, answerCn: `作为一种行动的激励。` },

          { type: "section", titleCn: "T40", descFr: "", descCn: "" },
          { id: 391, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在自己的奶酪里发现了某样东西` },
          { id: 392, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 393, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃了很多` },
          { id: 394, topicCn: "", answerFr: `D'analyser les moyens de séduire les jeunes`, answerCn: `分析吸引年轻人的方式` },
          { id: 395, topicCn: "", answerFr: `Ils jonglent entre vie privée et vie professionnelle`, answerCn: `他们在私人生活与工作之间周旋` },
          { id: 396, topicCn: "", answerFr: `Développer une identité commune`, answerCn: `建立共同身份认同` },
          { id: 397, topicCn: "", answerFr: `Le désir d'évolution durant la vie active`, answerCn: `职业生涯中的发展愿望` },
          { id: 398, topicCn: "", answerFr: `De l'organisation d'une animation clandestine`, answerCn: `组织秘密活动` },
          { id: 399, topicCn: "", answerFr: `Travailler sur soi-même`, answerCn: `自我提升` },
          { id: 400, topicCn: "", answerFr: `À chaque activité correspond une région précise`, answerCn: `每项活动对应一个特定地区` },
        ]

"""

# ---- Config ----
TACHE = 1             # change to 2/3 if you want
KIND = "a"               # "a" for answers; if you insist, change to "q"
OUT_CSV = Path("assets/tcfcaCE/t1.csv")
# ----------------


def extract_answerfr_strings(text: str) -> list[str]:
    """
    Extracts the quoted string after answerFr: "..."
    Assumes answerFr values use double quotes.
    """
    answers = []
    key = 'answerFr: `'
    i = 0
    n = len(text)

    while True:
        start = text.find(key, i)
        if start == -1:
            break
        j = start + len(key)

        # scan until the next unescaped quote
        buf = []
        esc = False
        while j < n:
            ch = text[j]
            if esc:
                buf.append(ch)
                esc = False
            else:
                if ch == "\\":
                    esc = True
                elif ch == '`':
                    break
                else:
                    buf.append(ch)
            j += 1

        answers.append("".join(buf).strip())
        i = j + 1

    # drop empties
    return [a for a in answers if a]


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
