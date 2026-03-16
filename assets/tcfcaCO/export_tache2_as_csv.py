#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
[

          // ── T01 ──
          { type: "section", titleCn: "T01", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Faire la preuve de son désir de travailler`, answerCn: `证明自己的工作意愿` },
          { id: 2, topicCn: "", answerFr: `Leur nom s'est transformé en label de prestige`, answerCn: `他们的名字已成为声望的标签` },
          { id: 3, topicCn: "", answerFr: `Des adaptations télévisées de Maupassant`, answerCn: `莫泊桑作品的电视改编` },
          { id: 4, topicCn: "", answerFr: `Entreprendre une rénovation du lieu`, answerCn: `对该场所进行翻新` },
          { id: 5, topicCn: "", answerFr: `C'est une réponse à des besoins alimentaires accrus`, answerCn: `这是对日益增长的饮食需求的回应` },
          { id: 6, topicCn: "", answerFr: `Les producteurs évitent de prendre des risques`, answerCn: `生产者避免承担风险` },
          { id: 7, topicCn: "", answerFr: `Pour rester maitre de sa vie privée`, answerCn: `为了保持对私生活的掌控` },
          { id: 8, topicCn: "", answerFr: `Une diminution de la diversité de la faune océanique`, answerCn: `海洋动物多样性的减少` },
          { id: 9, topicCn: "", answerFr: `Gagner de l'argent pour payer leur séjour`, answerCn: `赚钱支付住宿费用` },
          { id: 10, topicCn: "", answerFr: `Ils paraissent manipulés par une force supérieure`, answerCn: `他们似乎被某种更高的力量所操纵` },

          // ── T02 ──
          { type: "section", titleCn: "T02", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `De lutter contre les imitations`, answerCn: `抵制仿冒品` },
          { id: 2, topicCn: "", answerFr: `Imite à la perfection la voix d'un enfant`, answerCn: `完美地模仿儿童的声音` },
          { id: 3, topicCn: "", answerFr: `Son succès auprès des étudiants se dégrade`, answerCn: `它在学生中的受欢迎程度下降了` },
          { id: 4, topicCn: "", answerFr: `Dormir efficacement`, answerCn: `高效睡眠` },
          { id: 5, topicCn: "", answerFr: `À financer les travaux du château par un don`, answerCn: `通过捐款资助城堡的修缮工程` },
          { id: 6, topicCn: "", answerFr: `La diversité des portraits présentés`, answerCn: `所呈现人物肖像的多样性` },
          { id: 7, topicCn: "", answerFr: `Les gens en mangent plus que par le passé`, answerCn: `人们现在比过去吃得更多` },
          { id: 8, topicCn: "", answerFr: `Pour faire naître l'envie de s'investir dans un métier`, answerCn: `激发人们投身某一职业的热情` },
          { id: 9, topicCn: "", answerFr: `L'impartialité doit être l'une des qualités principales d'un maitre`, answerCn: `公正应是教师最重要的品质之一` },
          { id: 10, topicCn: "", answerFr: `Pour dissimuler la pauvreté des contenus`, answerCn: `掩盖内容的匮乏` },

          // ── T03 ──
          { type: "section", titleCn: "T03", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Envoyer des vœux de nouvel an`, answerCn: `发送新年祝福` },
          { id: 2, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众舆论` },
          { id: 3, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可以被用作控制工具` },
          { id: 4, topicCn: "", answerFr: `Le triomphe d'une opinion émise par Apollinaire mais autrefois combattue`, answerCn: `阿波利奈尔曾提出但一度受到抵制的观点最终获得认可` },
          { id: 5, topicCn: "", answerFr: `La fréquence de ses congénères`, answerCn: `同类的频率` },
          { id: 6, topicCn: "", answerFr: `Elle aura un meilleur pouvoir d'achat sous peu`, answerCn: `她不久将拥有更强的购买力` },
          { id: 7, topicCn: "", answerFr: `Les ressources en gaz à l'échelle mondiale s'accroissent`, answerCn: `全球天然气资源正在增加` },

          // ── T04 ──
          { type: "section", titleCn: "T04", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Démarrer une activité professionnelle`, answerCn: `开启一项职业活动` },
          { id: 2, topicCn: "", answerFr: `Faire rêver les petits patients`, answerCn: `让小患者充满梦想` },
          { id: 3, topicCn: "", answerFr: `Elle s'adresse exclusivement à une clientèle soucieuse des questions d'environnement`, answerCn: `它专门面向关注环境问题的客户群体` },
          { id: 4, topicCn: "", answerFr: `Faire prendre conscience des excès liés à leur usage`, answerCn: `使人意识到过度使用所带来的问题` },
          { id: 5, topicCn: "", answerFr: `D'aménager des réserves restreignant la pêche`, answerCn: `建立限制捕鱼的保护区` },
          { id: 6, topicCn: "", answerFr: `Les professeurs avec les compétences nécessaires sont rares`, answerCn: `具备必要能力的教师十分稀缺` },
          { id: 7, topicCn: "", answerFr: `Intégrer des valeurs sociales et environnementales`, answerCn: `融入社会和环境价值观` },
          { id: 8, topicCn: "", answerFr: `Le film tombe dans les stéréotypes du genre`, answerCn: `这部电影落入了该类型的套路` },
          { id: 9, topicCn: "", answerFr: `L'impartialité doit être l'une des qualités principales d'un maitre`, answerCn: `公正应是教师最重要的品质之一` },
          { id: 10, topicCn: "", answerFr: `Mettre en commun les données`, answerCn: `共享数据` },

          // ── T05 ──
          { type: "section", titleCn: "T05", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在奶酪里发现了什么东西` },
          { id: 2, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人接触` },
          { id: 3, topicCn: "", answerFr: `Pour participer à la finale d'un jeu`, answerCn: `参加游戏决赛` },
          { id: 4, topicCn: "", answerFr: `Dormir efficacement`, answerCn: `高效睡眠` },
          { id: 5, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 6, topicCn: "", answerFr: `Il a cherché à préserver la beauté du site`, answerCn: `他致力于保护该地点的美观` },
          { id: 7, topicCn: "", answerFr: `Ils développent leur culture du goût`, answerCn: `他们培养品味文化` },
          { id: 8, topicCn: "", answerFr: `Le gaspillage de l'eau dans le réseau domestique`, answerCn: `家庭供水系统中的水资源浪费` },
          { id: 9, topicCn: "", answerFr: `L'absence de programme politique`, answerCn: `缺乏政治纲领` },
          { id: 10, topicCn: "", answerFr: `Elles croyaient voir là leurs propres peintures`, answerCn: `她们以为看到的是自己的画作` },

          // ── T06 ──
          { type: "section", titleCn: "T06", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退款其商品` },
          { id: 2, topicCn: "", answerFr: `C'est possible mais pénible`, answerCn: `这是可能的，但很麻烦` },
          { id: 3, topicCn: "", answerFr: `Montrer l'importance de la chimie dans les rapports humains`, answerCn: `展示化学在人际关系中的重要性` },
          { id: 4, topicCn: "", answerFr: `Il estime qu'il reste du travail à faire pour mieux préparer cette évolution`, answerCn: `他认为仍有工作要做，以便更好地应对这一变化` },
          { id: 5, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `通过互联网，越来越多的用户可以访问它` },
          { id: 6, topicCn: "", answerFr: `Le jeu des interprètes`, answerCn: `演员的表演` },
          { id: 7, topicCn: "", answerFr: `Elle entraînera un gain financier`, answerCn: `它将带来经济收益` },
          { id: 8, topicCn: "", answerFr: `Pour faire naître l'envie de s'investir dans un métier`, answerCn: `激发人们投身某一职业的热情` },
          { id: 9, topicCn: "", answerFr: `Il transforme notre rapport au savoir`, answerCn: `它改变了我们与知识的关系` },
          { id: 10, topicCn: "", answerFr: `L'ambiguïté du néologisme « chat » à l'écrire`, answerCn: `书面新词"chat"的歧义性` },

          // ── T07 ──
          { type: "section", titleCn: "T07", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人接触` },
          { id: 2, topicCn: "", answerFr: `Qui ont de l'expérience dans la télévente`, answerCn: `具有电视销售经验的人` },
          { id: 3, topicCn: "", answerFr: `Du fait de sa taille`, answerCn: `由于其规模` },
          { id: 4, topicCn: "", answerFr: `Le changement est définitif`, answerCn: `这一变化是不可逆的` },
          { id: 5, topicCn: "", answerFr: `Les produits utilisés dans les cultures`, answerCn: `农业生产中使用的产品` },
          { id: 6, topicCn: "", answerFr: `En envoyant des courriels sur la plateforme de l'émission`, answerCn: `通过向节目平台发送电子邮件` },
          { id: 7, topicCn: "", answerFr: `L'image attachée à sa profession est stéréotypée et peu valorisante`, answerCn: `与其职业相关的形象是刻板且缺乏价值感的` },
          { id: 8, topicCn: "", answerFr: `D'un catalogue de styliste`, answerCn: `来自造型师目录` },
          { id: 9, topicCn: "", answerFr: `Son exploitation génère des revenus élevés`, answerCn: `其经营产生了高额收入` },
          { id: 10, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },

          // ── T08 ──
          { type: "section", titleCn: "T08", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 2, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 3, topicCn: "", answerFr: `Le besoin d'interaction social`, answerCn: `社交互动的需求` },
          { id: 4, topicCn: "", answerFr: `Elle trouve l'ensemble très réussi`, answerCn: `她认为整体效果非常成功` },
          { id: 5, topicCn: "", answerFr: `L'originalité des plats`, answerCn: `菜肴的独创性` },
          { id: 6, topicCn: "", answerFr: `Les professeurs avec des compétences nécessaires sont rares`, answerCn: `具备必要能力的教师十分稀缺` },
          { id: 7, topicCn: "", answerFr: `Faire la promotion de l'apprentissage d'un métier auprès des jeunes`, answerCn: `向年轻人推广职业学习` },
          { id: 8, topicCn: "", answerFr: `Elle modifie le rapport au temps`, answerCn: `它改变了人们与时间的关系` },
          { id: 9, topicCn: "", answerFr: `La générosité qu'elle manifestait dans sa vie`, answerCn: `她在生活中所展现的慷慨` },
          { id: 10, topicCn: "", answerFr: `Il déclare que la photographie était une part nécessaire, mais non essentielle à son travail`, answerCn: `他表示摄影是其工作的必要组成部分，但并非核心` },

          // ── T09 ──
          { type: "section", titleCn: "T09", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 2, topicCn: "", answerFr: `Faire part de la réponse d'un responsable`, answerCn: `转达负责人的回复` },
          { id: 3, topicCn: "", answerFr: `Il risque d'entraver la circulation des véhicules de secours`, answerCn: `可能妨碍救援车辆的通行` },
          { id: 4, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可以被用作控制工具` },
          { id: 5, topicCn: "", answerFr: `Elle masque les problèmes pédagogiques essentiels`, answerCn: `它掩盖了核心的教育问题` },
          { id: 6, topicCn: "", answerFr: `Faire la promotion de l'apprentissage d'un métier auprès des jeunes`, answerCn: `向年轻人推广职业学习` },
          { id: 7, topicCn: "", answerFr: `Les gens en mangent plus que par le passé`, answerCn: `人们现在比过去吃得更多` },
          { id: 8, topicCn: "", answerFr: `D'un catalogue de styliste`, answerCn: `来自造型师目录` },
          { id: 9, topicCn: "", answerFr: `La manipulation des clients par les industriels`, answerCn: `工业企业对消费者的操控` },
          { id: 10, topicCn: "", answerFr: `Le renoncement au nucléaire doit être mûrement planifié`, answerCn: `放弃核能必须经过深思熟虑的规划` },

          // ── T10 ──
          { type: "section", titleCn: "T10", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `En achetant les billets à l'avance`, answerCn: `提前购票` },
          { id: 2, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众舆论` },
          { id: 3, topicCn: "", answerFr: `Le besoin d'interaction sociale`, answerCn: `社交互动的需求` },
          { id: 4, topicCn: "", answerFr: `De faire un bilan de leurs aptitudes`, answerCn: `对自身能力进行评估` },
          { id: 5, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `通过互联网，越来越多的用户可以访问它` },
          { id: 6, topicCn: "", answerFr: `Le désir d'évolution durant la vie active`, answerCn: `职业生涯中的发展欲望` },
          { id: 7, topicCn: "", answerFr: `Ils se rendent régulièrement en ville`, answerCn: `他们定期前往城市` },
          { id: 8, topicCn: "", answerFr: `Elle modifie le rapport au temps`, answerCn: `它改变了人们与时间的关系` },
          { id: 9, topicCn: "", answerFr: `La générosité qu'elle manifestait dans sa vie`, answerCn: `她在生活中所展现的慷慨` },
          { id: 10, topicCn: "", answerFr: `À favoriser l'émergence de valeurs culturelles collectives`, answerCn: `促进集体文化价值观的形成` },

          // ── T11 ──
          { type: "section", titleCn: "T11", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在奶酪里发现了什么东西` },
          { id: 2, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 3, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃了很多` },
          { id: 4, topicCn: "", answerFr: `Des rendements en baisse`, answerCn: `产量下降` },
          { id: 5, topicCn: "", answerFr: `Mieux communiquer sur l'utilisation des fonds`, answerCn: `更好地传达资金使用情况` },
          { id: 6, topicCn: "", answerFr: `En envoyant des courriels sur la plateforme de l'émission`, answerCn: `通过向节目平台发送电子邮件` },
          { id: 7, topicCn: "", answerFr: `L'image attachée à sa profession est stéréotypée et peu valorisante`, answerCn: `与其职业相关的形象是刻板且缺乏价值感的` },
          { id: 8, topicCn: "", answerFr: `Obtenir de l'argent pour développer des centres d'accueil`, answerCn: `筹集资金以发展接待中心` },
          { id: 9, topicCn: "", answerFr: `L'harmonisation de leurs appellations`, answerCn: `统一其命名规范` },
          { id: 10, topicCn: "", answerFr: `Il constate la fréquence des modifications apportées aux photos`, answerCn: `他注意到照片被修改的频率很高` },

          // ── T12 ──
          { type: "section", titleCn: "T12", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Responsabiliser les acteurs concernés`, answerCn: `让相关责任方承担责任` },
          { id: 2, topicCn: "", answerFr: `À accueillir des artistes ainsi que leurs œuvres`, answerCn: `接待艺术家及其作品` },
          { id: 3, topicCn: "", answerFr: `L'homme se laisse dominer par la technologie`, answerCn: `人类被技术所支配` },
          { id: 4, topicCn: "", answerFr: `Le retard pris dans ses recherches`, answerCn: `其研究进度的滞后` },
          { id: 5, topicCn: "", answerFr: `Il a écrit une œuvre abondante et variée`, answerCn: `他创作了大量且多样化的作品` },
          { id: 6, topicCn: "", answerFr: `Le sport sans douleur`, answerCn: `无痛运动` },
          { id: 7, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 8, topicCn: "", answerFr: `Ils alternent les supports selon le type d'activité`, answerCn: `他们根据活动类型交替使用不同载体` },
          { id: 9, topicCn: "", answerFr: `à Paris et partout en Europe`, answerCn: `在巴黎及整个欧洲` },
          { id: 10, topicCn: "", answerFr: `Que son dossier est examiné`, answerCn: `其申请材料正在审核中` },

          // ── T13 ──
          { type: "section", titleCn: "T13", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Son humour fait passer un message sérieux`, answerCn: `他的幽默传递了严肃的信息` },
          { id: 2, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人接触` },
          { id: 3, topicCn: "", answerFr: `Des adaptations télévisées de Maupassant`, answerCn: `莫泊桑作品的电视改编` },
          { id: 4, topicCn: "", answerFr: `L'expansion de la concurrence internationale`, answerCn: `国际竞争的扩张` },
          { id: 5, topicCn: "", answerFr: `Ils sont plus sûrs de leur nouveau choix`, answerCn: `他们对新选择更有把握` },
          { id: 6, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 7, topicCn: "", answerFr: `Une mise en valeur de l'autre`, answerCn: `对他人的肯定与彰显` },
          { id: 8, topicCn: "", answerFr: `De simples citoyens`, answerCn: `普通公民` },
          { id: 9, topicCn: "", answerFr: `De la situation économique tendue`, answerCn: `经济形势紧张` },
          { id: 10, topicCn: "", answerFr: `Les recherches sont limitées par le manque d'informations`, answerCn: `研究受到信息匮乏的限制` },

          // ── T14 ──
          { type: "section", titleCn: "T14", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La technologie modifie la relation à la gastronomie`, answerCn: `技术改变了人们与美食的关系` },
          { id: 2, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退款其商品` },
          { id: 3, topicCn: "", answerFr: `C'est possible, mais pénible`, answerCn: `这是可能的，但很麻烦` },
          { id: 4, topicCn: "", answerFr: `Il estime qu'il reste du travail à faire pour mieux préparer cette évolution`, answerCn: `他认为仍有工作要做，以便更好地应对这一变化` },
          { id: 5, topicCn: "", answerFr: `D'aménager des réserves restreignant la pêche`, answerCn: `建立限制捕鱼的保护区` },
          { id: 6, topicCn: "", answerFr: `Ils permettent au système de se maintenir`, answerCn: `它们使该系统得以维持` },
          { id: 7, topicCn: "", answerFr: `Ils alternent les supports selon le type d'activité`, answerCn: `他们根据活动类型交替使用不同载体` },
          { id: 8, topicCn: "", answerFr: `D'un catalogue de styliste`, answerCn: `来自造型师目录` },
          { id: 9, topicCn: "", answerFr: `Son exploitation génère des revenus élevés`, answerCn: `其经营产生了高额收入` },
          { id: 10, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `耕作方法` },

          // ── T15 ──
          { type: "section", titleCn: "T15", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L'expression du temps est opposée à la représentation habituelle`, answerCn: `时间的表达与惯常的表现形式相反` },
          { id: 2, topicCn: "", answerFr: `Leur nom s'est transformé en Label de prestige`, answerCn: `他们的名字已成为声望的标签` },
          { id: 3, topicCn: "", answerFr: `Pour participer à la finale d'un jeu`, answerCn: `参加游戏决赛` },
          { id: 4, topicCn: "", answerFr: `De lutter contre la saleté dans la capitale`, answerCn: `在首都对抗脏乱问题` },
          { id: 5, topicCn: "", answerFr: `Ils sont financés discrètement par des entreprises`, answerCn: `它们受到企业的秘密资助` },
          { id: 6, topicCn: "", answerFr: `Intégrer des valeurs sociales et environnementales`, answerCn: `融入社会和环境价值观` },
          { id: 7, topicCn: "", answerFr: `Généraliser l'agriculture biologique`, answerCn: `推广有机农业` },
          { id: 8, topicCn: "", answerFr: `Une diminution de la diversité de la faune océanique`, answerCn: `海洋动物多样性的减少` },
          { id: 9, topicCn: "", answerFr: `Une manifestation culturelle`, answerCn: `一项文化活动` },
          { id: 10, topicCn: "", answerFr: `Pour dissimuler la pauvreté des contenus`, answerCn: `掩盖内容的匮乏` },

          // ── T16 ──
          { type: "section", titleCn: "T16", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a trouvé les causes du rétrécissement de la laine`, answerCn: `他找到了羊毛缩水的原因` },
          { id: 2, topicCn: "", answerFr: `Elle a diversifié son alimentation`, answerCn: `她使饮食多样化` },
          { id: 3, topicCn: "", answerFr: `Son succès auprès des étudiants se dégrade`, answerCn: `它在学生中的受欢迎程度下降了` },
          { id: 4, topicCn: "", answerFr: `Le personnel manque de chaleur et d'amabilité`, answerCn: `工作人员缺乏热情和亲切感` },
          { id: 5, topicCn: "", answerFr: `Ils sont financés discrètement par des entreprises`, answerCn: `它们受到企业的秘密资助` },
          { id: 6, topicCn: "", answerFr: `Du manque de familles d'accueil`, answerCn: `寄养家庭的短缺` },
          { id: 7, topicCn: "", answerFr: `La réelle dimension écologique du festival`, answerCn: `该节日真正的生态维度` },
          { id: 8, topicCn: "", answerFr: `Le message véhiculé par la publicité était inacceptable`, answerCn: `广告所传递的信息是不可接受的` },
          { id: 9, topicCn: "", answerFr: `Ce sont les violons récents qui sont les plus estimés`, answerCn: `近期制作的小提琴是最受推崇的` },

          // ── T17 ──
          { type: "section", titleCn: "T17", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Une perte de spontanéité des matchs`, answerCn: `比赛自发性的丧失` },
          { id: 2, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 3, topicCn: "", answerFr: `I nécessite une réorganisation des lieux les plus visités`, answerCn: `需要对最受欢迎的场所进行重新规划` },
          { id: 4, topicCn: "", answerFr: `C'est un carrefour culturel intercontinental`, answerCn: `这是一个跨洲际的文化交汇点` },
          { id: 5, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `通过互联网，越来越多的用户可以访问它` },
          { id: 6, topicCn: "", answerFr: `Pour obtenir des données sur sa composition`, answerCn: `以获取其成分数据` },
          { id: 7, topicCn: "", answerFr: `De nouvelles pédagogies semblent nécessaires`, answerCn: `新的教学方法似乎十分必要` },
          { id: 8, topicCn: "", answerFr: `Les doutes sur les méthodes de production`, answerCn: `对生产方法的疑虑` },
          { id: 9, topicCn: "", answerFr: `La manipulation des clients par les industriels`, answerCn: `工业企业对消费者的操控` },
          { id: 10, topicCn: "", answerFr: `Faire évoluer les mentalités au sujet du handicap au travail`, answerCn: `改变人们对职场残障问题的观念` },

          // ── T18 ──
          { type: "section", titleCn: "T18", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Son humour fait passer un message sérieux`, answerCn: `他的幽默传递了严肃的信息` },
          { id: 2, topicCn: "", answerFr: `Entrer en contact avec les gens`, answerCn: `与人接触` },
          { id: 3, topicCn: "", answerFr: `Elle masque les problèmes pédagogiques essentiels`, answerCn: `它掩盖了核心的教育问题` },
          { id: 4, topicCn: "", answerFr: `Entreprendre une rénovation du lieu`, answerCn: `对该场所进行翻新` },
          { id: 5, topicCn: "", answerFr: `Très peu de francophones occupent des fonctions à responsabilité`, answerCn: `很少有法语使用者担任有责任的职位` },
          { id: 6, topicCn: "", answerFr: `S'ils appartiennent à une espèce adéquate`, answerCn: `如果它们属于合适的物种` },
          { id: 7, topicCn: "", answerFr: `Généraliser l'agriculture biologique`, answerCn: `推广有机农业` },
          { id: 8, topicCn: "", answerFr: `Diminuer les risques sanitaires`, answerCn: `降低卫生健康风险` },
          { id: 9, topicCn: "", answerFr: `Le développement d'une conscience civique`, answerCn: `公民意识的培养` },
          { id: 10, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `耕作方法` },

          // ── T19 ──
          { type: "section", titleCn: "T19", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Présenter les relations familiales avec humour`, answerCn: `以幽默的方式呈现家庭关系` },
          { id: 2, topicCn: "", answerFr: `Une activité de maquillage`, answerCn: `化妆活动` },
          { id: 3, topicCn: "", answerFr: `De signaler sur les photos les modifications effectuées`, answerCn: `在照片上标注所做的修改` },
          { id: 4, topicCn: "", answerFr: `Le confort a été très nettement amélioré`, answerCn: `舒适度得到了显著改善` },
          { id: 5, topicCn: "", answerFr: `De nouvelles pratiques de vente`, answerCn: `新的销售实践` },
          { id: 6, topicCn: "", answerFr: `C'est une réclamation destinée au gérant d'un immeuble`, answerCn: `这是向楼宇管理员提出的投诉` },
          { id: 7, topicCn: "", answerFr: `Intégrer des valeurs sociales et environnementales`, answerCn: `融入社会和环境价值观` },
          { id: 8, topicCn: "", answerFr: `Empêcher le trafic des fromages de contrebande`, answerCn: `阻止走私奶酪的贸易` },
          { id: 9, topicCn: "", answerFr: `D'une pollution imperceptible`, answerCn: `难以察觉的污染` },
          { id: 10, topicCn: "", answerFr: `Ils paraissent manipulés par une force supérieure`, answerCn: `他们似乎被某种更高的力量所操纵` },

          // ── T20 ──
          { type: "section", titleCn: "T20", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Des séjours alliant détente et découvertes`, answerCn: `融合休闲与探索的旅居体验` },
          { id: 2, topicCn: "", answerFr: `Son ambiance créative`, answerCn: `其充满创意的氛围` },
          { id: 3, topicCn: "", answerFr: `Le confort a été très nettement amélioré`, answerCn: `舒适度得到了显著改善` },
          { id: 4, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃了很多` },
          { id: 5, topicCn: "", answerFr: `À financer les travaux du château par un don`, answerCn: `通过捐款资助城堡的修缮工程` },
          { id: 6, topicCn: "", answerFr: `Améliorer les relations au sein du lycée`, answerCn: `改善高中内部的人际关系` },
          { id: 7, topicCn: "", answerFr: `Trouver des valeurs communes`, answerCn: `寻找共同价值观` },
          { id: 8, topicCn: "", answerFr: `Il critique son concept`, answerCn: `他批评其概念` },
          { id: 9, topicCn: "", answerFr: `Ils perpétuent une forme d'exclusion`, answerCn: `它们延续了一种排斥形式` },
          { id: 10, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `耕作方法` },

          // ── T21 ──
          { type: "section", titleCn: "T21", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il explique l'idée de départ d'un livre de Modiano`, answerCn: `他解释了莫迪亚诺一本书的创作初衷` },
          { id: 2, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退款其商品` },
          { id: 3, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `挑选一件纪念品` },
          { id: 4, topicCn: "", answerFr: `Elle entraine une trop grande consommation d'énergie`, answerCn: `它导致了过高的能源消耗` },
          { id: 5, topicCn: "", answerFr: `Ils sont financés discrètement par des entreprises`, answerCn: `它们受到企业的秘密资助` },
          { id: 6, topicCn: "", answerFr: `Par la primauté de l'intérêt collectif sur bénéfices`, answerCn: `以集体利益优先于盈利` },
          { id: 7, topicCn: "", answerFr: `L'image attachée à sa profession est stéréotypée et peu valorisante`, answerCn: `与其职业相关的形象是刻板且缺乏价值感的` },
          { id: 8, topicCn: "", answerFr: `Il envisage avec optimisme les futurs possibles`, answerCn: `他乐观地展望各种可能的未来` },
          { id: 9, topicCn: "", answerFr: `À quel problème sont confrontés les distributeurs indépendants`, answerCn: `独立发行商面临什么问题` },
          { id: 10, topicCn: "", answerFr: `Travailler sur soi-même`, answerCn: `自我提升` },

          // ── T22 ──
          { type: "section", titleCn: "T22", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il explique l'idée de départ d'un livre de Modiano`, answerCn: `他解释了莫迪亚诺一本书的创作初衷` },
          { id: 2, topicCn: "", answerFr: `Une activité de maquillage`, answerCn: `化妆活动` },
          { id: 3, topicCn: "", answerFr: `Être amateur de viande et militer pour le bien-être animal`, answerCn: `既是肉食爱好者，又倡导动物福利` },
          { id: 4, topicCn: "", answerFr: `Définir les conditions d'accueil des élèves en milieu professionnel`, answerCn: `规定学生在职业环境中的接待条件` },
          { id: 5, topicCn: "", answerFr: `Il est accessible à un nombre croissant d'utilisateurs grâce à internet`, answerCn: `通过互联网，越来越多的用户可以访问它` },
          { id: 6, topicCn: "", answerFr: `Pour obtenir des données sur sa composition`, answerCn: `以获取其成分数据` },
          { id: 7, topicCn: "", answerFr: `L'essor de nouveaux modes de consommation`, answerCn: `新消费模式的兴起` },
          { id: 8, topicCn: "", answerFr: `Organiser des séjours à vocation humanitaire`, answerCn: `组织以人道主义为目的的旅居活动` },
          { id: 9, topicCn: "", answerFr: `Il est difficile d'en évaluer l'impact sur la santé`, answerCn: `难以评估其对健康的影响` },
          { id: 10, topicCn: "", answerFr: `Pour dissimuler la pauvreté des contenus`, answerCn: `掩盖内容的匮乏` },

          // ── T23 ──
          { type: "section", titleCn: "T23", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Leur nom s'est transformé en label de prestige`, answerCn: `他们的名字已成为声望的标签` },
          { id: 2, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退款其商品` },
          { id: 3, topicCn: "", answerFr: `D'analyser les moyens de séduire les jeunes`, answerCn: `分析吸引年轻人的方式` },
          { id: 4, topicCn: "", answerFr: `Elle permet de dépenser moins d'argent`, answerCn: `它可以减少开支` },
          { id: 5, topicCn: "", answerFr: `L'originalité des plats`, answerCn: `菜肴的独创性` },
          { id: 6, topicCn: "", answerFr: `Un rappel d'un impayé en cours`, answerCn: `催缴未付款项的提醒` },
          { id: 7, topicCn: "", answerFr: `Elle répond de manière pertinente aux difficultés et aux aspirations des élèves`, answerCn: `它切实回应了学生的困难和期望` },
          { id: 8, topicCn: "", answerFr: `Obtenir de l'argent pour développer des centres d'accueil`, answerCn: `筹集资金以发展接待中心` },
          { id: 9, topicCn: "", answerFr: `Des outils de communication`, answerCn: `沟通工具` },
          { id: 10, topicCn: "", answerFr: `L'ambiguïté du néologisme « chat » à l'écrit`, answerCn: `书面新词"chat"的歧义性` },

          // ── T24 ──
          { type: "section", titleCn: "T24", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La technologie modifie la relation à la gastronomie`, answerCn: `技术改变了人们与美食的关系` },
          { id: 2, topicCn: "", answerFr: `Pour créer un lien entre générations`, answerCn: `为了建立代际联系` },
          { id: 3, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `挑选一件纪念品` },
          { id: 4, topicCn: "", answerFr: `Il a acclamé de toutes ses forces la chanteuse`, answerCn: `他全力为这位歌手喝彩` },
          { id: 5, topicCn: "", answerFr: `D'aménager des réserves restreignant la pêche`, answerCn: `建立限制捕鱼的保护区` },
          { id: 6, topicCn: "", answerFr: `De vérifier le profil des postulants`, answerCn: `核实申请者的资料` },
          { id: 7, topicCn: "", answerFr: `Une mise en valeur de l'autre`, answerCn: `对他人的肯定与彰显` },
          { id: 8, topicCn: "", answerFr: `Elle modifie le rapport au temps`, answerCn: `它改变了人们与时间的关系` },
          { id: 9, topicCn: "", answerFr: `Transmettre des connaissances`, answerCn: `传授知识` },
          { id: 10, topicCn: "", answerFr: `Que ses écrits permettent de mieux cerner qu'il était`, answerCn: `他的文字有助于更好地了解他是怎样的人` },

          // ── T25 ──
          { type: "section", titleCn: "T25", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 2, topicCn: "", answerFr: `Le public se reconnaît à travers le héros`, answerCn: `观众通过主人公产生共鸣` },
          { id: 3, topicCn: "", answerFr: `À une simulation de mission spatiale`, answerCn: `模拟太空任务` },
          { id: 4, topicCn: "", answerFr: `Être titulaire d'une formation reconnue`, answerCn: `拥有认可的学历` },
          { id: 5, topicCn: "", answerFr: `Favoriser l'égalité des chances`, answerCn: `促进机会平等` },
          { id: 6, topicCn: "", answerFr: `L'optimisation de leur gestion est en cours d'étude`, answerCn: `其管理优化正在研究中` },
          { id: 7, topicCn: "", answerFr: `Les producteurs évitent de prendre des risques`, answerCn: `生产者避免承担风险` },
          { id: 8, topicCn: "", answerFr: `Elle abrite une vie animée`, answerCn: `这里生活活跃` },
          { id: 9, topicCn: "", answerFr: `Choisir des actions pour leur commune`, answerCn: `为社区选择行动方案` },
          { id: 10, topicCn: "", answerFr: `Il appartient à une réflexion philosophique`, answerCn: `它属于哲学思考` },

          // ── T26 ──
          { type: "section", titleCn: "T26", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il explique l'idée de départ d'un livre de Modiano`, answerCn: `他解释了莫迪亚诺一本书的创作初衷` },
          { id: 2, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众舆论` },
          { id: 3, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可以被用作控制工具` },
          { id: 4, topicCn: "", answerFr: `De faire un bilan de leurs aptitudes`, answerCn: `对自身能力进行评估` },
          { id: 5, topicCn: "", answerFr: `Ils intègrent l'ancien à leurs constructions`, answerCn: `他们将旧元素融入其建筑中` },
          { id: 6, topicCn: "", answerFr: `Les grandes surfaces provoquent la fin des petites boutiques de quartier`, answerCn: `大型超市导致街区小商店的消亡` },
          { id: 7, topicCn: "", answerFr: `De la volonté d'émancipation`, answerCn: `解放意愿` },
          { id: 8, topicCn: "", answerFr: `Il remet en question leurs retombées positives`, answerCn: `他质疑其积极效应` },
          { id: 9, topicCn: "", answerFr: `Le développement d'une conscience civique`, answerCn: `公民意识的培养` },
          { id: 10, topicCn: "", answerFr: `Faire évoluer les mentalités au sujet du handicap au travail`, answerCn: `改变人们对职场残障问题的观念` },

          // ── T27 ──
          { type: "section", titleCn: "T27", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle récolte les produits de terrains privés`, answerCn: `她采集私人土地上的产品` },
          { id: 2, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 3, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `挑选一件纪念品` },
          { id: 4, topicCn: "", answerFr: `Il a écrit une œuvre abondante et variée`, answerCn: `他创作了大量且多样化的作品` },
          { id: 5, topicCn: "", answerFr: `Elles contribuent à protéger l'environnement`, answerCn: `它们有助于保护环境` },
          { id: 6, topicCn: "", answerFr: `Il sera proche d'un jardin public`, answerCn: `它将毗邻一座公共花园` },
          { id: 7, topicCn: "", answerFr: `Elle est modelée par ses locuteurs`, answerCn: `它由其使用者所塑造` },
          { id: 8, topicCn: "", answerFr: `Respecter les normes internationales`, answerCn: `遵守国际标准` },
          { id: 9, topicCn: "", answerFr: `Démontrer les dégâts des méthodes de culture intensive`, answerCn: `揭示集约化耕作方法的危害` },
          { id: 10, topicCn: "", answerFr: `Elle est incompatible avec les objets politiques`, answerCn: `它与政治目标不相容` },

          // ── T28 ──
          { type: "section", titleCn: "T28", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在奶酪里发现了什么东西` },
          { id: 2, topicCn: "", answerFr: `Actrice à la télévision française`, answerCn: `法国电视台演员` },
          { id: 3, topicCn: "", answerFr: `Elle a diversifié son alimentation`, answerCn: `她使饮食多样化` },
          { id: 4, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `挑选一件纪念品` },
          { id: 5, topicCn: "", answerFr: `Le triomphe d'une opinion émise par Apollinaire, mais autrefois combattue`, answerCn: `阿波利奈尔曾提出但一度受到抵制的观点最终获得认可` },
          { id: 6, topicCn: "", answerFr: `De vérifier le profil des postulants`, answerCn: `核实申请者的资料` },
          { id: 7, topicCn: "", answerFr: `Il remet en question leurs retombées positives`, answerCn: `他质疑其积极效应` },
          { id: 8, topicCn: "", answerFr: `La coopération de ses membres`, answerCn: `其成员之间的合作` },
          { id: 9, topicCn: "", answerFr: `Elles représentent inégalement les milieux sociaux`, answerCn: `它们对社会各阶层的呈现不均衡` },
          { id: 10, topicCn: "", answerFr: `Les recherches sont limitées par le manque d'informations`, answerCn: `研究受到信息匮乏的限制` },

          // ── T29 ──
          { type: "section", titleCn: "T29", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle récolte les produits de terrains privés`, answerCn: `她采集私人土地上的产品` },
          { id: 2, topicCn: "", answerFr: `Imite à la perfection la voix d'un enfant`, answerCn: `完美地模仿儿童的声音` },
          { id: 3, topicCn: "", answerFr: `Ils permettent de protéger la biodiversité`, answerCn: `它们有助于保护生物多样性` },
          { id: 4, topicCn: "", answerFr: `Il a écrit une œuvre abondante et variée`, answerCn: `他创作了大量且多样化的作品` },
          { id: 5, topicCn: "", answerFr: `Elles contribuent à protéger l'environnement`, answerCn: `它们有助于保护环境` },
          { id: 6, topicCn: "", answerFr: `En révisant les conditions de rémunération`, answerCn: `通过修订薪酬条件` },
          { id: 7, topicCn: "", answerFr: `Elle est modelée par ses locuteurs`, answerCn: `它由其使用者所塑造` },
          { id: 8, topicCn: "", answerFr: `Il critique son concept`, answerCn: `他批评其概念` },
          { id: 9, topicCn: "", answerFr: `Transmettre des connaissances`, answerCn: `传授知识` },
          { id: 10, topicCn: "", answerFr: `Elles modifient nos processus cognitifs`, answerCn: `它们改变了我们的认知过程` },

          // ── T30 ──
          { type: "section", titleCn: "T30", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle peut perdre son statut de langue dominante`, answerCn: `它可能失去主导语言的地位` },
          { id: 2, topicCn: "", answerFr: `Une perte de spontanéité des matchs`, answerCn: `比赛自发性的丧失` },
          { id: 3, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 4, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃了很多` },
          { id: 5, topicCn: "", answerFr: `La réforme des retraites influencera leurs comportements`, answerCn: `退休制度改革将影响他们的行为` },
          { id: 6, topicCn: "", answerFr: `À une simulation de mission spatiale`, answerCn: `模拟太空任务` },
          { id: 7, topicCn: "", answerFr: `On ignore comment elles ont été réalisées`, answerCn: `人们不知道它们是如何完成的` },
          { id: 8, topicCn: "", answerFr: `Cela favorise l'intégration de nouvelles espèces et est bon pour l'écosystème`, answerCn: `这有利于新物种的融入，对生态系统有益` },
          { id: 9, topicCn: "", answerFr: `Interpréter certains rôles`, answerCn: `扮演某些角色` },
          { id: 10, topicCn: "", answerFr: `Démontrer les dégâts des méthodes de culture intensive`, answerCn: `揭示集约化耕作方法的危害` },

          // ── T31 ──
          { type: "section", titleCn: "T31", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La technologie modifie la relation à la gastronomie`, answerCn: `技术改变了人们与美食的关系` },
          { id: 2, topicCn: "", answerFr: `L'adaptation de l'offre culinaire à la mode actuelle`, answerCn: `烹饪供应对当前潮流的适应` },
          { id: 3, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `挑选一件纪念品` },
          { id: 4, topicCn: "", answerFr: `Elle soutient l'esprit de création`, answerCn: `它支持创造精神` },
          { id: 5, topicCn: "", answerFr: `Ils sont plus sûrs de leur nouveau choix`, answerCn: `他们对新选择更有把握` },
          { id: 6, topicCn: "", answerFr: `Ils permettent au système de se maintenir`, answerCn: `它们使该系统得以维持` },
          { id: 7, topicCn: "", answerFr: `De nouvelles pédagogies semblent nécessaires`, answerCn: `新的教学方法似乎十分必要` },
          { id: 8, topicCn: "", answerFr: `Le nombre d'ouvrages à paraître a diminué`, answerCn: `待出版书籍数量减少了` },
          { id: 9, topicCn: "", answerFr: `Ils perpétuent une forme d'exclusion`, answerCn: `它们延续了一种排斥形式` },
          { id: 10, topicCn: "", answerFr: `Elles contribuent à une bonne hygiène de vie`, answerCn: `它们有助于养成良好的生活卫生习惯` },

          // ── T32 ──
          { type: "section", titleCn: "T32", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle récolte les produits de terrains privés`, answerCn: `她采集私人土地上的产品` },
          { id: 2, topicCn: "", answerFr: `Avoir la garantie de la qualité du produit et ignorer d'où il vient`, answerCn: `获得产品质量保证同时不知道其来源` },
          { id: 3, topicCn: "", answerFr: `Ils peuvent être utilisés comme outils de contrôle`, answerCn: `它们可以被用作控制工具` },
          { id: 4, topicCn: "", answerFr: `Elle associe différentes formes d'expression artistique`, answerCn: `它结合了不同形式的艺术表达` },
          { id: 5, topicCn: "", answerFr: `Il soutient les entreprises locales`, answerCn: `它支持本地企业` },
          { id: 6, topicCn: "", answerFr: `Pour soutenir les agriculteurs de proximité`, answerCn: `为了支持本地农民` },
          { id: 7, topicCn: "", answerFr: `Les ressources en gaz à l'échelle mondiale s'accroissent`, answerCn: `全球天然气资源正在增加` },
          { id: 8, topicCn: "", answerFr: `De l'organisation d'une animation clandestine`, answerCn: `秘密活动的组织` },
          { id: 9, topicCn: "", answerFr: `Une manifestation culturelle`, answerCn: `一项文化活动` },
          { id: 10, topicCn: "", answerFr: `La mise en oeuvre d'une action collective`, answerCn: `集体行动的实施` },

          // ── T33 ──
          { type: "section", titleCn: "T33", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `En achetant les billets à l'avance`, answerCn: `提前购票` },
          { id: 2, topicCn: "", answerFr: `L'organisation d'un événement culturel`, answerCn: `文化活动的组织` },
          { id: 3, topicCn: "", answerFr: `Il risque d'entraver la circulation des véhicules de secours`, answerCn: `可能妨碍救援车辆的通行` },
          { id: 4, topicCn: "", answerFr: `Pour proposer davantage de places`, answerCn: `为了提供更多座位` },
          { id: 5, topicCn: "", answerFr: `Ouvrir une bibliothèque pour tous`, answerCn: `向所有人开放图书馆` },
          { id: 6, topicCn: "", answerFr: `La diversité des portraits présentés`, answerCn: `所呈现人物肖像的多样性` },
          { id: 7, topicCn: "", answerFr: `Pour dénoncer le manque d'entretien`, answerCn: `为了揭露维护不足的问题` },
          { id: 8, topicCn: "", answerFr: `Le film tombe dans les stéréotypes du genre`, answerCn: `这部电影落入了该类型的套路` },
          { id: 9, topicCn: "", answerFr: `Le recrutement de personnels qualifiés`, answerCn: `招募合格人员` },
          { id: 10, topicCn: "", answerFr: `Demander à une cliente de payer l'intégralité de sa commande`, answerCn: `要求顾客全额支付订单` },

          // ── T34 ──
          { type: "section", titleCn: "T34", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un espace de remise en forme`, answerCn: `一个健身空间` },
          { id: 2, topicCn: "", answerFr: `Maintenir les performances de la mémoire`, answerCn: `保持记忆能力` },
          { id: 3, topicCn: "", answerFr: `Sélectionner un souvenir`, answerCn: `挑选一件纪念品` },
          { id: 4, topicCn: "", answerFr: `Il a acclamé de toutes ses forces la chanteuse`, answerCn: `他全力为这位歌手喝彩` },
          { id: 5, topicCn: "", answerFr: `Pour proposer davantage de places`, answerCn: `为了提供更多座位` },
          { id: 6, topicCn: "", answerFr: `Mieux communiquer sur L'utilisation des fonds`, answerCn: `更好地传达资金使用情况` },
          { id: 7, topicCn: "", answerFr: `Trouver des valeurs communes`, answerCn: `寻找共同价值观` },
          { id: 8, topicCn: "", answerFr: `Diversifier les activités en centre-ville`, answerCn: `使市中心的活动多样化` },
          { id: 9, topicCn: "", answerFr: `De la situation économique tendue`, answerCn: `经济形势紧张` },
          { id: 10, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },

          // ── T35 ──
          { type: "section", titleCn: "T35", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L'adaptation de l'offre culinaire à la mode actuelle`, answerCn: `烹饪供应对当前潮流的适应` },
          { id: 2, topicCn: "", answerFr: `Le remboursement de son article`, answerCn: `退款其商品` },
          { id: 3, topicCn: "", answerFr: `Il influence la productivité des salariés`, answerCn: `它影响员工的生产效率` },
          { id: 4, topicCn: "", answerFr: `La multiplication des éclairages publics`, answerCn: `公共照明设施的增加` },
          { id: 5, topicCn: "", answerFr: `Il facilite la lecture des étiquettes`, answerCn: `它便于阅读标签` },
          { id: 6, topicCn: "", answerFr: `Ils incitent leur entourage à les imiter`, answerCn: `他们鼓励周围的人效仿` },
          { id: 7, topicCn: "", answerFr: `Elle répond aux tendances actuelles`, answerCn: `它顺应当前潮流` },
          { id: 8, topicCn: "", answerFr: `Le nombre d'ouvrages à paraître a diminué`, answerCn: `待出版书籍数量减少了` },
          { id: 9, topicCn: "", answerFr: `La mise en œuvre d'une action collective`, answerCn: `集体行动的实施` },
          { id: 10, topicCn: "", answerFr: `Les méthodes de culture`, answerCn: `耕作方法` },

          // ── T36 ──
          { type: "section", titleCn: "T36", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Pour créer un lien entre générations`, answerCn: `为了建立代际联系` },
          { id: 2, topicCn: "", answerFr: `Une activité de maquillage`, answerCn: `化妆活动` },
          { id: 3, topicCn: "", answerFr: `De signaler sur les photos les modifications effectuées`, answerCn: `在照片上标注所做的修改` },
          { id: 4, topicCn: "", answerFr: `Il influence la productivité des salariés`, answerCn: `它影响员工的生产效率` },
          { id: 5, topicCn: "", answerFr: `L'expansion de la concurrence internationale`, answerCn: `国际竞争的扩张` },
          { id: 6, topicCn: "", answerFr: `Il facilite la lecture des étiquettes`, answerCn: `它便于阅读标签` },
          { id: 7, topicCn: "", answerFr: `Il se propage imperceptiblement`, answerCn: `它悄然蔓延` },
          { id: 8, topicCn: "", answerFr: `Décrire les rapports du sport et de la politique internationale`, answerCn: `描述体育与国际政治之间的关系` },
          { id: 9, topicCn: "", answerFr: `Travailler sur soi-même`, answerCn: `自我提升` },
          { id: 10, topicCn: "", answerFr: `Il est indissociable de celui des savoirs`, answerCn: `它与知识的发展密不可分` },

          // ── T37 ──
          { type: "section", titleCn: "T37", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Créer un site collaboratif de données`, answerCn: `创建一个协作数据网站` },
          { id: 2, topicCn: "", answerFr: `Il modifie le moment du coucher`, answerCn: `它改变了就寝时间` },
          { id: 3, topicCn: "", answerFr: `De limiter le gaspillage alimentaire`, answerCn: `减少食物浪费` },
          { id: 4, topicCn: "", answerFr: `Le besoin d'interaction sociale`, answerCn: `社交互动的需求` },
          { id: 5, topicCn: "", answerFr: `Aux étincelles produites par des perturbations orageuses`, answerCn: `由雷暴扰动产生的火花` },
          { id: 6, topicCn: "", answerFr: `Rebelle à toute forme d'autorité`, answerCn: `反抗一切形式的权威` },
          { id: 7, topicCn: "", answerFr: `Le malentendu sur le lieu où est enterré Brassens`, answerCn: `关于布拉桑斯安葬地点的误解` },
          { id: 8, topicCn: "", answerFr: `Les doutes sur les méthodes de production`, answerCn: `对生产方法的疑虑` },
          { id: 9, topicCn: "", answerFr: `Elles gagnent en visibilité dans ce milieu`, answerCn: `她们在这一领域获得了更多曝光` },
          { id: 10, topicCn: "", answerFr: `Elles modifient nos processus cognitifs`, answerCn: `它们改变了我们的认知过程` },

          // ── T38 ──
          { type: "section", titleCn: "T38", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Des séjours alliant détente et découvertes`, answerCn: `融合休闲与探索的旅居体验` },
          { id: 2, topicCn: "", answerFr: `La prise en compte de l'opinion publique`, answerCn: `考虑公众舆论` },
          { id: 3, topicCn: "", answerFr: `C'est possible mais pénible`, answerCn: `这是可能的，但很麻烦` },
          { id: 4, topicCn: "", answerFr: `Pour donner une bonne image d'eux`, answerCn: `为了树立良好的自身形象` },
          { id: 5, topicCn: "", answerFr: `Faire découvrir les formations pour devenir ingénieur`, answerCn: `介绍成为工程师的培训课程` },
          { id: 6, topicCn: "", answerFr: `Il peut s'étendre au domaine personnel`, answerCn: `它可以延伸至个人领域` },
          { id: 7, topicCn: "", answerFr: `De la volonté d'émancipation`, answerCn: `解放意愿` },
          { id: 8, topicCn: "", answerFr: `Le respect de la déontologie médicale est primordial`, answerCn: `遵守医疗职业道德至关重要` },
          { id: 9, topicCn: "", answerFr: `Des outils ont été élaborés pour en estimer l'intensité`, answerCn: `已开发出工具来评估其强度` },
          { id: 10, topicCn: "", answerFr: `Il donne un conseil`, answerCn: `他给出一条建议` },

          // ── T39 ──
          { type: "section", titleCn: "T39", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Le secret d'une bonne préparation`, answerCn: `良好备赛的秘诀` },
          { id: 2, topicCn: "", answerFr: `Présenter les relations familiales avec humour`, answerCn: `以幽默的方式呈现家庭关系` },
          { id: 3, topicCn: "", answerFr: `C'est possible mais pénible`, answerCn: `这是可能的，但很麻烦` },
          { id: 4, topicCn: "", answerFr: `Pour donner une bonne image d'eux`, answerCn: `为了树立良好的自身形象` },
          { id: 5, topicCn: "", answerFr: `Parce que l'événement s'inscrit dans un principe d'universalité`, answerCn: `因为该活动遵循普遍性原则` },
          { id: 6, topicCn: "", answerFr: `Les produits utilisés dans les cultures`, answerCn: `农业生产中使用的产品` },
          { id: 7, topicCn: "", answerFr: `La bonne humeur garantit de meilleures performances`, answerCn: `愉快的心情保证更好的表现` },
          { id: 8, topicCn: "", answerFr: `Le message véhiculé par la publicité était inacceptable`, answerCn: `广告所传递的信息是不可接受的` },
          { id: 9, topicCn: "", answerFr: `Ils s'impliquent de façon responsable dans les cours`, answerCn: `他们以负责任的方式参与课堂` },
          { id: 10, topicCn: "", answerFr: `Comme une incitation à l'action`, answerCn: `作为行动的激励` },

          // ── T40 ──
          { type: "section", titleCn: "T40", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在奶酪里发现了什么东西` },
          { id: 2, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试新的冒险` },
          { id: 3, topicCn: "", answerFr: `Parce que les larves ont beaucoup mangé`, answerCn: `因为幼虫吃了很多` },
          { id: 4, topicCn: "", answerFr: `D'analyser les moyens de séduire les jeunes`, answerCn: `分析吸引年轻人的方式` },
          { id: 5, topicCn: "", answerFr: `Ils jonglent entre vie privée et vie professionnelle`, answerCn: `他们在私人生活和职业生活之间游刃有余` },
          { id: 6, topicCn: "", answerFr: `Développer une identité commune`, answerCn: `培养共同认同感` },
          { id: 7, topicCn: "", answerFr: `Le désir d'évolution durant la vie active`, answerCn: `职业生涯中的发展欲望` },
          { id: 8, topicCn: "", answerFr: `De l'organisation d'une animation clandestine`, answerCn: `秘密活动的组织` },
          { id: 9, topicCn: "", answerFr: `Travailler sur soi-même`, answerCn: `自我提升` },
          { id: 10, topicCn: "", answerFr: `À chaque activité correspond une région précise`, answerCn: `每项活动对应一个特定地区` },

        ];

"""

# ---- Config ----
TACHE = 2             # change to 2/3 if you want
KIND = "a"               # "a" for answers; if you insist, change to "q"
OUT_CSV = Path("assets/tcfcaCO/t2.csv")
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
