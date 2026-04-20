#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
[
          { type: "section", titleCn: "T01", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Une publicité à faible coût`, answerCn: `低成本的广告` },
          { id: 2, topicCn: "", answerFr: `Pour s’installer dans un local plus vaste`, answerCn: `为了搬进一个更宽敞的场所` },
          { id: 3, topicCn: "", answerFr: `Acheter du matériel`, answerCn: `购买设备` },
          { id: 4, topicCn: "", answerFr: `Marrakech`, answerCn: `马拉喀什` },
          { id: 5, topicCn: "", answerFr: `Il fait observer la nature de façon différente`, answerCn: `它让人以不同的方式观察自然` },
          { id: 6, topicCn: "", answerFr: `On les a attrapés et emmenés ailleurs`, answerCn: `他们被抓住并带到了别处` },
          { id: 7, topicCn: "", answerFr: `L’enseignement est d’un bon niveau`, answerCn: `教学水平不错` },
          { id: 8, topicCn: "", answerFr: `Le rôle est peu valorisé`, answerCn: `这一角色不太受重视` },
          { id: 9, topicCn: "", answerFr: `Elle peut perdre son statut de langue dominante`, answerCn: `它可能失去主导语言的地位` },

          { type: "section", titleCn: "T02", descFr: "", descCn: "" },
          { id: 10, topicCn: "", answerFr: `Pour un réveillon`, answerCn: `为了节日前夜聚会` },
          { id: 11, topicCn: "", answerFr: `D’argent pour la course`, answerCn: `用于采购的钱` },
          { id: 12, topicCn: "", answerFr: `De poser leurs jours de vacances`, answerCn: `安排他们的休假天数` },
          { id: 13, topicCn: "", answerFr: `Donner des conseils pour arrêter de recevoir des publicités`, answerCn: `提供停止接收广告的建议` },
          { id: 14, topicCn: "", answerFr: `Il permettra d’éviter les embouteillages en ville`, answerCn: `它将有助于避免城市交通堵塞` },
          { id: 15, topicCn: "", answerFr: `Pour respecter des normes d’hygiène`, answerCn: `为了遵守卫生标准` },
          { id: 16, topicCn: "", answerFr: `Pratiquer la course à pied plusieurs fois par semaine`, answerCn: `每周跑步几次` },
          { id: 17, topicCn: "", answerFr: `Rencontrer les candidats sans rien savoir d’eux`, answerCn: `在对候选人一无所知的情况下与他们见面` },
          { id: 18, topicCn: "", answerFr: `De pratiquer un sport`, answerCn: `进行一项体育运动` },

          { type: "section", titleCn: "T03", descFr: "", descCn: "" },
          { id: 19, topicCn: "", answerFr: `Dialoguer avec le personnel enseignant`, answerCn: `与教师人员交流` },
          { id: 20, topicCn: "", answerFr: `De manger quotidiennement du chocolat`, answerCn: `每天吃巧克力` },
          { id: 21, topicCn: "", answerFr: `Elles habitent dans le même pays`, answerCn: `她们住在同一个国家` },
          { id: 22, topicCn: "", answerFr: `La nécessité de s’exiler pour pouvoir travailler`, answerCn: `为了能够工作而不得不背井离乡` },
          { id: 23, topicCn: "", answerFr: `De permettre aux enfants de faire leur travail du soir en classe`, answerCn: `让孩子们在课堂上完成晚上的作业` },
          { id: 24, topicCn: "", answerFr: `D’encourager les personnes handicapées à faire du sport`, answerCn: `鼓励残障人士进行体育运动` },
          { id: 25, topicCn: "", answerFr: `Leur curiosité`, answerCn: `他们的好奇心` },
          { id: 26, topicCn: "", answerFr: `Une méthode pour choisir une formation.`, answerCn: `一种选择培训的方法` },
          { id: 27, topicCn: "", answerFr: `Téléphoner à l’entreprise`, answerCn: `给公司打电话` },

          { type: "section", titleCn: "T04", descFr: "", descCn: "" },
          { id: 28, topicCn: "", answerFr: `S’informer sur le monde professionnel`, answerCn: `了解职业世界` },
          { id: 29, topicCn: "", answerFr: `S’aventurent dans les pays lointains`, answerCn: `他们冒险前往遥远的国家` },
          { id: 30, topicCn: "", answerFr: `Elles ont besoin d'accompagnement`, answerCn: `她们需要陪伴和指导` },
          { id: 31, topicCn: "", answerFr: `En France`, answerCn: `在法国` },
          { id: 32, topicCn: "", answerFr: `Leur curiosité`, answerCn: `他们的好奇心` },
          { id: 33, topicCn: "", answerFr: `De les utiliser comme monnaie`, answerCn: `把它们当作货币使用` },
          { id: 34, topicCn: "", answerFr: `Faire la preuve de son désir de travailler`, answerCn: `证明自己有工作的意愿` },
          { id: 35, topicCn: "", answerFr: `En achetant les billets en avance`, answerCn: `通过提前买票` },
          { id: 36, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试一次新的冒险` },

          { type: "section", titleCn: "T05", descFr: "", descCn: "" },
          { id: 37, topicCn: "", answerFr: `Un voyage en train couchettes`, answerCn: `一次卧铺列车之旅` },
          { id: 38, topicCn: "", answerFr: `De pratiquer leur sport différemment`, answerCn: `以不同方式进行他们的运动` },
          { id: 39, topicCn: "", answerFr: `Un candidat à des études supérieures`, answerCn: `一名高等教育申请者` },
          { id: 40, topicCn: "", answerFr: `Assister à des spectacles`, answerCn: `观看演出` },
          { id: 41, topicCn: "", answerFr: `Il faut se remettre à bouger de façon régulière`, answerCn: `必须重新开始规律地运动起来` },
          { id: 42, topicCn: "", answerFr: `Des vêtements en tissus non traités`, answerCn: `由未经处理的布料制成的衣物` },
          { id: 43, topicCn: "", answerFr: `Ils permettent un contact direct avec un écran tactile`, answerCn: `它们可以让人直接接触触摸屏` },
          { id: 44, topicCn: "", answerFr: `Faire de ces boîtiers des moments de partage`, answerCn: `把这些盒子变成分享交流的时刻` },
          { id: 45, topicCn: "", answerFr: `Un service de prêt à domicile`, answerCn: `一项上门借阅服务` },

          { type: "section", titleCn: "T06", descFr: "", descCn: "" },
          { id: 46, topicCn: "", answerFr: `Pour prévenir leurs voisins de leur fête`, answerCn: `为了提前告知邻居他们要办聚会` },
          { id: 47, topicCn: "", answerFr: `De voir Lyon d’une façon différente`, answerCn: `以一种不同的方式看里昂` },
          { id: 48, topicCn: "", answerFr: `L’anniversaire d’un magasin`, answerCn: `一家商店的周年纪念` },
          { id: 49, topicCn: "", answerFr: `Annoncer la sortie d’un roman`, answerCn: `宣布一本小说出版` },
          { id: 50, topicCn: "", answerFr: `Une familiarisation avec les codes socio professionnels français`, answerCn: `熟悉法国社会职业规范` },
          { id: 51, topicCn: "", answerFr: `Une victoire de Brice Leverdez`, answerCn: `布里斯·勒韦尔德兹的一场胜利` },
          { id: 52, topicCn: "", answerFr: `Pratiquer la course à pied plusieurs fois par semaine`, answerCn: `每周跑步几次` },
          { id: 53, topicCn: "", answerFr: `Des spécialités locales`, answerCn: `当地特产` },
          { id: 54, topicCn: "", answerFr: `Le bruit altère le sens du goût des passagers`, answerCn: `噪音会削弱乘客的味觉` },

          { type: "section", titleCn: "T07", descFr: "", descCn: "" },
          { id: 55, topicCn: "", answerFr: `À choisir ses produits`, answerCn: `帮助选择产品` },
          { id: 56, topicCn: "", answerFr: `Agent de sécurité`, answerCn: `保安人员` },
          { id: 57, topicCn: "", answerFr: `D’envoyer des photos`, answerCn: `发送照片` },
          { id: 58, topicCn: "", answerFr: `Elles habitent dans le même pays`, answerCn: `她们住在同一个国家` },
          { id: 59, topicCn: "", answerFr: `La nécessité de s’exiler pour pouvoir travailler`, answerCn: `为了能够工作而不得不背井离乡` },
          { id: 60, topicCn: "", answerFr: `Ils permettent un contact direct avec un écran tactile`, answerCn: `它们可以让人直接接触触摸屏` },
          { id: 61, topicCn: "", answerFr: `Enthousiaste pour le restaurant`, answerCn: `对这家餐厅很热情` },
          { id: 62, topicCn: "", answerFr: `Une visite guidée originale`, answerCn: `一次别出心裁的导览参观` },
          { id: 63, topicCn: "", answerFr: `Il explique l’idée de départ d’un livre de Modiano`, answerCn: `他解释了一本莫迪亚诺作品最初的构想` },

          { type: "section", titleCn: "T08", descFr: "", descCn: "" },
          { id: 64, topicCn: "", answerFr: `Faire de la musique avec d’autres personnes`, answerCn: `和其他人一起做音乐` },
          { id: 65, topicCn: "", answerFr: `Leur forme`, answerCn: `它们的形状` },
          { id: 66, topicCn: "", answerFr: `Elle est bonne pour la santé`, answerCn: `它对健康有益` },
          { id: 67, topicCn: "", answerFr: `Elle les revend d’occasion`, answerCn: `她把它们当二手转卖` },
          { id: 68, topicCn: "", answerFr: `Travailler dans une maison d’édition`, answerCn: `在出版社工作` },
          { id: 69, topicCn: "", answerFr: `Dans la protection des droits`, answerCn: `在权利保护方面` },
          { id: 70, topicCn: "", answerFr: `Des enregistrements sonores d’article de journal`, answerCn: `报纸文章的录音` },
          { id: 71, topicCn: "", answerFr: `Aux locataires qui ont de faibles revenus`, answerCn: `面向低收入租户` },
          { id: 72, topicCn: "", answerFr: `Le bruit altère le sens du goût des passagers`, answerCn: `噪音会削弱乘客的味觉` },

          { type: "section", titleCn: "T09", descFr: "", descCn: "" },
          { id: 73, topicCn: "", answerFr: `Faire de la musique avec d’autres personnes`, answerCn: `和其他人一起做音乐` },
          { id: 74, topicCn: "", answerFr: `Pour éviter de tomber malades`, answerCn: `为了避免生病` },
          { id: 75, topicCn: "", answerFr: `Il peut partager sa passion avec un public`, answerCn: `他可以与公众分享自己的热情` },
          { id: 76, topicCn: "", answerFr: `Donner une famille aux enfants`, answerCn: `给孩子们一个家庭` },
          { id: 77, topicCn: "", answerFr: `Les Parisiens peuvent accéder facilement à des livres électroniques`, answerCn: `巴黎人可以方便地获取电子书` },
          { id: 78, topicCn: "", answerFr: `Il est passionné d’ouvrages sur les langues`, answerCn: `他痴迷于语言类书籍` },
          { id: 79, topicCn: "", answerFr: `Consulter sa boîte de réception de courriels`, answerCn: `查看自己的电子邮件收件箱` },
          { id: 80, topicCn: "", answerFr: `Aux locataires qui ont de faibles revenus`, answerCn: `面向低收入租户` },
          { id: 81, topicCn: "", answerFr: `Il explique l’idée de départ d’un livre de Modiano`, answerCn: `他解释了一本莫迪亚诺作品最初的构想` },

          { type: "section", titleCn: "T10", descFr: "", descCn: "" },
          { id: 82, topicCn: "", answerFr: `Faire des courses`, answerCn: `买东西` },
          { id: 83, topicCn: "", answerFr: `Pour favoriser une autre pédagogie`, answerCn: `为了促进另一种教学方式` },
          { id: 84, topicCn: "", answerFr: `Leur forme`, answerCn: `它们的形状` },
          { id: 85, topicCn: "", answerFr: `Leur rendement au travail diminue`, answerCn: `他们的工作效率下降` },
          { id: 86, topicCn: "", answerFr: `Ils se connectent en toute liberté`, answerCn: `他们可以自由连接上网` },
          { id: 87, topicCn: "", answerFr: `De réutiliser des objets`, answerCn: `重新利用物品` },
          { id: 88, topicCn: "", answerFr: `Ils obtiennent des conseils sur le mode d’emploi`, answerCn: `他们获得有关使用方法的建议` },
          { id: 89, topicCn: "", answerFr: `Les échanges en famille s’améliorent`, answerCn: `家庭交流有所改善` },
          { id: 90, topicCn: "", answerFr: `Il permet d’être plus détendu`, answerCn: `它让人更加放松` },

          { type: "section", titleCn: "T11", descFr: "", descCn: "" },
          { id: 91, topicCn: "", answerFr: `À conseiller le promeneur`, answerCn: `给散步者提供建议` },
          { id: 92, topicCn: "", answerFr: `Faciliter la recherche d’emploi`, answerCn: `方便找工作` },
          { id: 93, topicCn: "", answerFr: `C’est un spécialiste du sujet`, answerCn: `他是这方面的专家` },
          { id: 94, topicCn: "", answerFr: `Goûter des recettes`, answerCn: `品尝食谱中的菜肴` },
          { id: 95, topicCn: "", answerFr: `La nécessité de s’exiler pour pouvoir travailler`, answerCn: `为了能够工作而不得不背井离乡` },
          { id: 96, topicCn: "", answerFr: `Signaler les difficultés de circulation`, answerCn: `报告通行困难` },
          { id: 97, topicCn: "", answerFr: `Effectuer des tâches administratives`, answerCn: `完成行政任务` },
          { id: 98, topicCn: "", answerFr: `Aux locataires qui ont de faibles revenus`, answerCn: `面向低收入租户` },
          { id: 99, topicCn: "", answerFr: `De lutter contre les imitations`, answerCn: `打击仿冒品` },

          { type: "section", titleCn: "T12", descFr: "", descCn: "" },
          { id: 100, topicCn: "", answerFr: `Oui, grâce à des méthodes très simples`, answerCn: `可以，借助一些非常简单的方法` },
          { id: 101, topicCn: "", answerFr: `Pour favoriser une autre pédagogie`, answerCn: `为了促进另一种教学方式` },
          { id: 102, topicCn: "", answerFr: `Elle souhaite des renseignements`, answerCn: `她想获取一些信息` },
          { id: 103, topicCn: "", answerFr: `Partager son appartement pour deux mois`, answerCn: `把自己的公寓短租两个月` },
          { id: 104, topicCn: "", answerFr: `Présenter de nouveaux produits`, answerCn: `展示新产品` },
          { id: 105, topicCn: "", answerFr: `Créer des emplois`, answerCn: `创造就业岗位` },
          { id: 106, topicCn: "", answerFr: `Faire la preuve de son désir de travailler`, answerCn: `证明自己有工作的意愿` },
          { id: 107, topicCn: "", answerFr: `Présenter les relations familiales avec humour`, answerCn: `以幽默方式展现家庭关系` },
          { id: 108, topicCn: "", answerFr: `Tenter une nouvelle aventure`, answerCn: `尝试一次新的冒险` },

          { type: "section", titleCn: "T13", descFr: "", descCn: "" },
          { id: 109, topicCn: "", answerFr: `Une boisson gratuite`, answerCn: `一杯免费饮料` },
          { id: 110, topicCn: "", answerFr: `De voir Lyon d’une façon différente`, answerCn: `以一种不同的方式看里昂` },
          { id: 111, topicCn: "", answerFr: `De manger quotidiennement du chocolat`, answerCn: `每天吃巧克力` },
          { id: 112, topicCn: "", answerFr: `Rencontrer des stars du cinéma`, answerCn: `见到电影明星` },
          { id: 113, topicCn: "", answerFr: `Ils répondent aux questions des internautes`, answerCn: `他们回答网友的问题` },
          { id: 114, topicCn: "", answerFr: `Un métier`, answerCn: `一种职业` },
          { id: 115, topicCn: "", answerFr: `On s’en méfie en France`, answerCn: `在法国人们对它持谨慎态度` },
          { id: 116, topicCn: "", answerFr: `Les étiquettes trompeuses`, answerCn: `具有误导性的标签` },
          { id: 117, topicCn: "", answerFr: `Créer un site collaboratif de données`, answerCn: `创建一个协作式数据网站` },

          { type: "section", titleCn: "T14", descFr: "", descCn: "" },
          { id: 118, topicCn: "", answerFr: `Des valises`, answerCn: `行李箱` },
          { id: 119, topicCn: "", answerFr: `Pour s’installer dans un local plus vaste`, answerCn: `为了搬进一个更宽敞的场所` },
          { id: 120, topicCn: "", answerFr: `D’argent pour la course`, answerCn: `用于采购的钱` },
          { id: 121, topicCn: "", answerFr: `Il va arriver en retard chez lui`, answerCn: `他回家会迟到` },
          { id: 122, topicCn: "", answerFr: `Goûter des recettes`, answerCn: `品尝食谱中的菜肴` },
          { id: 123, topicCn: "", answerFr: `Il a réussi à séduire un public local`, answerCn: `他成功吸引了当地观众` },
          { id: 124, topicCn: "", answerFr: `D’un homme qui produit des œuvres originales`, answerCn: `关于一个创作原创作品的人` },
          { id: 125, topicCn: "", answerFr: `Une méthode pour choisir une formation`, answerCn: `一种选择培训的方法` },
          { id: 126, topicCn: "", answerFr: `Le secret d’une bonne préparation`, answerCn: `良好准备的秘诀` },

          { type: "section", titleCn: "T15", descFr: "", descCn: "" },
          { id: 127, topicCn: "", answerFr: `Une publicité à faible coût`, answerCn: `低成本的广告` },
          { id: 128, topicCn: "", answerFr: `Sur la somme qu’elle a coûtée`, answerCn: `关于它花了多少钱` },
          { id: 129, topicCn: "", answerFr: `La rapidité de sa construction`, answerCn: `它建造的速度` },
          { id: 130, topicCn: "", answerFr: `Transporter des personnes`, answerCn: `运送人员` },
          { id: 131, topicCn: "", answerFr: `Les clubs disparaissaient vite après leur création`, answerCn: `这些俱乐部在创建后很快就消失了` },
          { id: 132, topicCn: "", answerFr: `D’organiser des échanges de longue durée`, answerCn: `组织长期交流活动` },
          { id: 133, topicCn: "", answerFr: `Un accompagnement personnalisé`, answerCn: `个性化辅导` },
          { id: 134, topicCn: "", answerFr: `Pour marcher sans souffrir`, answerCn: `为了走路时不受痛苦` },
          { id: 135, topicCn: "", answerFr: `Satisfaire la demande en produits biologiques locaux`, answerCn: `满足对本地有机产品的需求` },

          { type: "section", titleCn: "T16", descFr: "", descCn: "" },
          { id: 136, topicCn: "", answerFr: `Pour lui proposer de passer le voir avec son amie`, answerCn: `为了提议他和女友一起去看她` },
          { id: 137, topicCn: "", answerFr: `Faciliter la recherche d’emploi`, answerCn: `方便找工作` },
          { id: 138, topicCn: "", answerFr: `Ils donnent accès au sauna`, answerCn: `它们可以进入桑拿房` },
          { id: 139, topicCn: "", answerFr: `Faire plus attention au bruit`, answerCn: `更加注意噪音` },
          { id: 140, topicCn: "", answerFr: `Assister à un spectacle`, answerCn: `观看一场演出` },
          { id: 141, topicCn: "", answerFr: `Un jeu`, answerCn: `一个游戏` },
          { id: 142, topicCn: "", answerFr: `La réduction des effectifs de l’entreprise`, answerCn: `公司裁员` },
          { id: 143, topicCn: "", answerFr: `Il permet d’être plus détendu`, answerCn: `它让人更加放松` },
          { id: 144, topicCn: "", answerFr: `Il a trouvé quelque chose dans son fromage`, answerCn: `他在奶酪里发现了什么东西` },

          { type: "section", titleCn: "T17", descFr: "", descCn: "" },
          { id: 145, topicCn: "", answerFr: `De collecter du plastique`, answerCn: `收集塑料` },
          { id: 146, topicCn: "", answerFr: `Elle est bonne pour la santé`, answerCn: `它对健康有益` },
          { id: 147, topicCn: "", answerFr: `Annuler son achat`, answerCn: `取消购买` },
          { id: 148, topicCn: "", answerFr: `Assister à des spectacles`, answerCn: `观看演出` },
          { id: 149, topicCn: "", answerFr: `Les clubs disparaissaient vite après leur création`, answerCn: `这些俱乐部在创建后很快就消失了` },
          { id: 150, topicCn: "", answerFr: `Pour respecter des normes d’hygiène`, answerCn: `为了遵守卫生标准` },
          { id: 151, topicCn: "", answerFr: `De traiter seul des affections bénignes`, answerCn: `自行处理一些轻微疾病` },
          { id: 152, topicCn: "", answerFr: `Une offre intéressante`, answerCn: `一项很有吸引力的优惠` },
          { id: 153, topicCn: "", answerFr: `Faire de ces loisirs des moments de partage`, answerCn: `让这些休闲活动成为分享交流的时刻` },

          { type: "section", titleCn: "T18", descFr: "", descCn: "" },
          { id: 154, topicCn: "", answerFr: `Elle réunit les caractéristiques de deux continents`, answerCn: `它结合了两个大洲的特征` },
          { id: 155, topicCn: "", answerFr: `De faire un don`, answerCn: `进行捐赠` },
          { id: 156, topicCn: "", answerFr: `Jouer dans un film`, answerCn: `参演一部电影` },
          { id: 157, topicCn: "", answerFr: `D’envoyer des photos`, answerCn: `发送照片` },
          { id: 158, topicCn: "", answerFr: `Goûter des recettes`, answerCn: `品尝食谱中的菜肴` },
          { id: 159, topicCn: "", answerFr: `Exercer un travail satisfaisant`, answerCn: `从事一份令人满意的工作` },
          { id: 160, topicCn: "", answerFr: `Son ambiance créative`, answerCn: `它富有创意的氛围` },
          { id: 161, topicCn: "", answerFr: `Ils comprennent mieux l’intérêt des apprentissages proposés`, answerCn: `他们更能理解所提供学习内容的意义` },
          { id: 162, topicCn: "", answerFr: `Ils modifient les aptitudes mentales`, answerCn: `它们会改变心理能力` },

          { type: "section", titleCn: "T19", descFr: "", descCn: "" },
          { id: 163, topicCn: "", answerFr: `Faire des courses`, answerCn: `买东西` },
          { id: 164, topicCn: "", answerFr: `Faciliter la recherche d’emploi`, answerCn: `方便找工作` },
          { id: 165, topicCn: "", answerFr: `Une chambre chez l’habitant`, answerCn: `住在居民家中的一个房间` },
          { id: 166, topicCn: "", answerFr: `Vérifier sa consommation`, answerCn: `检查自己的消费情况` },
          { id: 167, topicCn: "", answerFr: `Des travaux sur la ligne`, answerCn: `线路施工` },
          { id: 168, topicCn: "", answerFr: `D’un lieu d’accueil`, answerCn: `关于一个接待场所` },
          { id: 169, topicCn: "", answerFr: `La pression de la société`, answerCn: `社会压力` },
          { id: 170, topicCn: "", answerFr: `Elle permet d’améliorer ses performances`, answerCn: `它能够提高自身表现` },
          { id: 171, topicCn: "", answerFr: `Son humour fait passer un message sérieux`, answerCn: `他的幽默传达了一个严肃的信息` },

          { type: "section", titleCn: "T20", descFr: "", descCn: "" },
          { id: 172, topicCn: "", answerFr: `Un travail avec des enfants`, answerCn: `一份和孩子们打交道的工作` },
          { id: 173, topicCn: "", answerFr: `Baisser certains tarifs`, answerCn: `降低某些价格` },
          { id: 174, topicCn: "", answerFr: `De l’aide pour une association`, answerCn: `给一个协会提供帮助` },
          { id: 175, topicCn: "", answerFr: `Découvrir des monuments connus`, answerCn: `参观著名的古迹` },
          { id: 176, topicCn: "", answerFr: `Trois ans d’expérience professionnelle`, answerCn: `三年职业经验` },
          { id: 177, topicCn: "", answerFr: `Les œuvres de peintres du début du 20e siècle`, answerCn: `20世纪初画家的作品` },
          { id: 178, topicCn: "", answerFr: `Apprendre des gestes pour protéger l’environnement`, answerCn: `学习保护环境的做法` },
          { id: 179, topicCn: "", answerFr: `Rencontrer les candidats sans rien savoir d’eux`, answerCn: `在对候选人一无所知的情况下与他们见面` },
          { id: 180, topicCn: "", answerFr: `Le secret d’une bonne préparation`, answerCn: `良好准备的秘诀` },

          { type: "section", titleCn: "T21", descFr: "", descCn: "" },
          { id: 181, topicCn: "", answerFr: `À choisir ses produits`, answerCn: `帮助选择产品` },
          { id: 182, topicCn: "", answerFr: `L’échanger`, answerCn: `把它换掉` },
          { id: 183, topicCn: "", answerFr: `Analyser leurs effets`, answerCn: `分析它们的影响` },
          { id: 184, topicCn: "", answerFr: `Goûter des recettes`, answerCn: `品尝食谱中的菜肴` },
          { id: 185, topicCn: "", answerFr: `De l’utilisation du portable`, answerCn: `关于手机的使用` },
          { id: 186, topicCn: "", answerFr: `Faire des courses dans un magasin`, answerCn: `在商店里购物` },
          { id: 187, topicCn: "", answerFr: `De visiter une grande exposition`, answerCn: `去参观一个大型展览` },
          { id: 188, topicCn: "", answerFr: `La durée de la représentation`, answerCn: `演出的时长` },
          { id: 189, topicCn: "", answerFr: `Le secret d’une bonne préparation`, answerCn: `良好准备的秘诀` },

          { type: "section", titleCn: "T22", descFr: "", descCn: "" },
          { id: 190, topicCn: "", answerFr: `Des activités pour l’été`, answerCn: `一些夏季活动` },
          { id: 191, topicCn: "", answerFr: `De pratiquer leur sport différemment`, answerCn: `以不同方式进行他们的运动` },
          { id: 192, topicCn: "", answerFr: `Un candidat a des études supérieures`, answerCn: `一名接受过高等教育的候选人` },
          { id: 193, topicCn: "", answerFr: `D’une idée nouvelle de recyclage`, answerCn: `关于一个新的回收理念` },
          { id: 194, topicCn: "", answerFr: `Ils s’exercent sans interruption dans l’année`, answerCn: `他们全年不间断地训练` },
          { id: 195, topicCn: "", answerFr: `On va arrêter de les vendre`, answerCn: `人们将停止出售它们` },
          { id: 196, topicCn: "", answerFr: `Faire des courses dans un magasin`, answerCn: `在商店里购物` },
          { id: 197, topicCn: "", answerFr: `La pression de la société`, answerCn: `社会压力` },
          { id: 198, topicCn: "", answerFr: `Ils comprennent mieux l’intérêt des apprentissages proposés`, answerCn: `他们更能理解所提供学习内容的意义` },

          { type: "section", titleCn: "T23", descFr: "", descCn: "" },
          { id: 199, topicCn: "", answerFr: `Téléphoner aux horaires indiqués`, answerCn: `在注明的时间打电话` },
          { id: 200, topicCn: "", answerFr: `Un message d’excuse`, answerCn: `一条道歉信息` },
          { id: 201, topicCn: "", answerFr: `De libérer les lieux pendant les travaux`, answerCn: `在施工期间腾空场地` },
          { id: 202, topicCn: "", answerFr: `Il présente des films réalisés par des personnes sourdes`, answerCn: `它展映由聋人拍摄的电影` },
          { id: 203, topicCn: "", answerFr: `Marrakech`, answerCn: `马拉喀什` },
          { id: 204, topicCn: "", answerFr: `Une manière originale de rencontrer des gens près de chez elle`, answerCn: `一种在她家附近结识他人的新颖方式` },
          { id: 205, topicCn: "", answerFr: `Pour marcher sans souffrir`, answerCn: `为了走路时不受痛苦` },
          { id: 206, topicCn: "", answerFr: `Mieux comprendre les préférences alimentaires des enfants`, answerCn: `更好地理解孩子们的饮食偏好` },
          { id: 207, topicCn: "", answerFr: `L’enquête policière d’une personne très rationnelle`, answerCn: `一个非常理性的人展开的刑事调查` },

          { type: "section", titleCn: "T24", descFr: "", descCn: "" },
          { id: 208, topicCn: "", answerFr: `Pour échanger des conseils sur le vélo`, answerCn: `为了交流骑行方面的建议` },
          { id: 209, topicCn: "", answerFr: `De voir Lyon d’une façon différente`, answerCn: `以一种不同的方式看里昂` },
          { id: 210, topicCn: "", answerFr: `D’argent pour la course`, answerCn: `用于采购的钱` },
          { id: 211, topicCn: "", answerFr: `Elle propose une découverte du Japon`, answerCn: `它提供一次对日本的探索体验` },
          { id: 212, topicCn: "", answerFr: `Pour faire des économies de papier`, answerCn: `为了节省纸张` },
          { id: 213, topicCn: "", answerFr: `Un lieu de livraison`, answerCn: `一个送货地点` },
          { id: 214, topicCn: "", answerFr: `D’un homme qui produit des œuvres originales`, answerCn: `关于一个创作原创作品的人` },
          { id: 215, topicCn: "", answerFr: `On veut les préserver durablement`, answerCn: `人们希望长期保护它们` },
          { id: 216, topicCn: "", answerFr: `Elle est déjà finie`, answerCn: `它已经结束了` },

          { type: "section", titleCn: "T25", descFr: "", descCn: "" },
          { id: 217, topicCn: "", answerFr: `De faire un repas entre voisins`, answerCn: `在邻居之间一起吃顿饭` },
          { id: 218, topicCn: "", answerFr: `Faire des courses dans un magasin`, answerCn: `在商店里购物` },
          { id: 219, topicCn: "", answerFr: `Elle est bonne pour la santé`, answerCn: `它对健康有益` },
          { id: 220, topicCn: "", answerFr: `L’offre spéciale de l’été`, answerCn: `夏季特别优惠` },
          { id: 221, topicCn: "", answerFr: `Faire ses courses plus rapidement`, answerCn: `更快地购物` },
          { id: 222, topicCn: "", answerFr: `De dormir au milieu de la nature`, answerCn: `在大自然中睡觉` },
          { id: 223, topicCn: "", answerFr: `Pour clarifier ses idées`, answerCn: `为了理清思路` },
          { id: 224, topicCn: "", answerFr: `Il donne un conseil`, answerCn: `他提出一个建议` },
          { id: 225, topicCn: "", answerFr: `Si c’est le fruit d’une décision personnelle`, answerCn: `如果这是个人决定的结果` },

          { type: "section", titleCn: "T26", descFr: "", descCn: "" },
          { id: 226, topicCn: "", answerFr: `Lister leurs besoins de matériel`, answerCn: `列出他们所需的设备` },
          { id: 227, topicCn: "", answerFr: `Ils ont fait le plein à très bas prix`, answerCn: `他们以很低的价格加满了油` },
          { id: 228, topicCn: "", answerFr: `Pour éviter de tomber malades`, answerCn: `为了避免生病` },
          { id: 229, topicCn: "", answerFr: `Présenter de nouveaux produits`, answerCn: `展示新产品` },
          { id: 230, topicCn: "", answerFr: `Assister à un spectacle`, answerCn: `观看一场演出` },
          { id: 231, topicCn: "", answerFr: `De développer des projets collectifs pour la ville`, answerCn: `为城市发展集体项目` },
          { id: 232, topicCn: "", answerFr: `Créer des emplois`, answerCn: `创造就业岗位` },
          { id: 233, topicCn: "", answerFr: `Il permet d’être plus détendu`, answerCn: `它让人更加放松` },
          { id: 234, topicCn: "", answerFr: `Elle est déjà finie`, answerCn: `它已经结束了` },

          { type: "section", titleCn: "T27", descFr: "", descCn: "" },
          { id: 235, topicCn: "", answerFr: `De les protéger de la chaleur`, answerCn: `为了保护它们免受高温影响` },
          { id: 236, topicCn: "", answerFr: `De participer à un jeu`, answerCn: `参加一个游戏` },
          { id: 237, topicCn: "", answerFr: `Il va arriver en retard chez lui`, answerCn: `他回家会迟到` },
          { id: 238, topicCn: "", answerFr: `En France`, answerCn: `在法国` },
          { id: 239, topicCn: "", answerFr: `Accueillir les patients avec bienveillance`, answerCn: `亲切地接待病人` },
          { id: 240, topicCn: "", answerFr: `De bien choisir une formation`, answerCn: `好好选择一个培训` },
          { id: 241, topicCn: "", answerFr: `Pourquoi dormir ?`, answerCn: `为什么要睡觉？` },
          { id: 242, topicCn: "", answerFr: `Faciliter le retour à l’emploi des mères`, answerCn: `促进母亲重返职场` },
          { id: 243, topicCn: "", answerFr: `Son humour fait passer un message sérieux`, answerCn: `他的幽默传达了一个严肃的信息` },

          { type: "section", titleCn: "T28", descFr: "", descCn: "" },
          { id: 244, topicCn: "", answerFr: `Pour lui proposer de passer le voir avec son amie`, answerCn: `为了提议他和女友一起去看她` },
          { id: 245, topicCn: "", answerFr: `De devenir membre de l’orchestre municipal`, answerCn: `成为市立乐团的一员` },
          { id: 246, topicCn: "", answerFr: `Une chambre chez l’habitant`, answerCn: `住在居民家中的一个房间` },
          { id: 247, topicCn: "", answerFr: `L’assistance d’une personne`, answerCn: `一个人的帮助` },
          { id: 248, topicCn: "", answerFr: `Les dangers des aliments mal conservés`, answerCn: `保存不当食物的危险` },
          { id: 249, topicCn: "", answerFr: `De réutiliser des objets`, answerCn: `重新利用物品` },
          { id: 250, topicCn: "", answerFr: `De visiter une grande exposition`, answerCn: `去参观一个大型展览` },
          { id: 251, topicCn: "", answerFr: `Les étiquettes trompeuses`, answerCn: `具有误导性的标签` },
          { id: 252, topicCn: "", answerFr: `Elle est déjà finie`, answerCn: `它已经结束了` },

          { type: "section", titleCn: "T29", descFr: "", descCn: "" },
          { id: 253, topicCn: "", answerFr: `La transformation d’un logement`, answerCn: `一个住房的改造` },
          { id: 254, topicCn: "", answerFr: `Faciliter la recherche d’emploi`, answerCn: `方便找工作` },
          { id: 255, topicCn: "", answerFr: `Leur forme`, answerCn: `它们的形状` },
          { id: 256, topicCn: "", answerFr: `Apporter à boire`, answerCn: `带些喝的来` },
          { id: 257, topicCn: "", answerFr: `De se reposer et de découvrir le milieu marin`, answerCn: `去休息并探索海洋环境` },
          { id: 258, topicCn: "", answerFr: `La France demeure une petite productrice sur le plan européen`, answerCn: `从欧洲范围来看，法国仍然是一个产量较小的生产国` },
          { id: 259, topicCn: "", answerFr: `Des enregistrements sonores d’articles de journaux`, answerCn: `报纸文章的录音` },
          { id: 260, topicCn: "", answerFr: `À leur dimension`, answerCn: `按照他们的尺寸` },
          { id: 261, topicCn: "", answerFr: `Réaliser une étude d’observation des astres`, answerCn: `开展一项天体观测研究` },

          { type: "section", titleCn: "T30", descFr: "", descCn: "" },
          { id: 262, topicCn: "", answerFr: `De dormir au milieu de la nature`, answerCn: `在大自然中睡觉` },
          { id: 263, topicCn: "", answerFr: `Elle est bonne pour la santé`, answerCn: `它对健康有益` },
          { id: 264, topicCn: "", answerFr: `Faire ses courses plus rapidement`, answerCn: `更快地购物` },
          { id: 265, topicCn: "", answerFr: `Elles ont besoin d’accompagnement`, answerCn: `她们需要陪伴和指导` },
          { id: 266, topicCn: "", answerFr: `Goûter des recettes`, answerCn: `品尝食谱中的菜肴` },
          { id: 267, topicCn: "", answerFr: `Faire des courses dans un magasin`, answerCn: `在商店里购物` },
          { id: 268, topicCn: "", answerFr: `Elle abrite une vie animée`, answerCn: `它孕育着活跃的生命` },
          { id: 269, topicCn: "", answerFr: `Les producteurs évitent de prendre des risques`, answerCn: `生产者避免承担风险` },
          { id: 270, topicCn: "", answerFr: `De lutter contre les imitations`, answerCn: `打击仿冒品` },

          { type: "section", titleCn: "T31", descFr: "", descCn: "" },
          { id: 271, topicCn: "", answerFr: `De collecter du plastique`, answerCn: `收集塑料` },
          { id: 272, topicCn: "", answerFr: `L’anniversaire d’un magasin`, answerCn: `一家商店的周年纪念` },
          { id: 273, topicCn: "", answerFr: `De préparer un entretien d’embauche`, answerCn: `准备一场求职面试` },
          { id: 274, topicCn: "", answerFr: `Assister à des spectacles`, answerCn: `观看演出` },
          { id: 275, topicCn: "", answerFr: `De l’utilisation du portable`, answerCn: `关于手机的使用` },
          { id: 276, topicCn: "", answerFr: `De réutiliser des objets`, answerCn: `重新利用物品` },
          { id: 277, topicCn: "", answerFr: `Elle est dans sa famille`, answerCn: `她在自己的家庭里` },
          { id: 278, topicCn: "", answerFr: `Ils comprennent mieux l’intérêt des apprentissages proposés`, answerCn: `他们更能理解所提供学习内容的意义` },
          { id: 279, topicCn: "", answerFr: `Les personnes qui y travaillent`, answerCn: `在那里工作的人` },

          { type: "section", titleCn: "T32", descFr: "", descCn: "" },
          { id: 280, topicCn: "", answerFr: `De dormir au milieu de la nature`, answerCn: `在大自然中睡觉` },
          { id: 281, topicCn: "", answerFr: `L’anniversaire d’un magasin`, answerCn: `一家商店的周年纪念` },
          { id: 282, topicCn: "", answerFr: `Se couvrir la gorge`, answerCn: `把喉咙捂好` },
          { id: 283, topicCn: "", answerFr: `Découvrir des instruments de musique`, answerCn: `发现各种乐器` },
          { id: 284, topicCn: "", answerFr: `Participer à la rédaction d’articles`, answerCn: `参与撰写文章` },
          { id: 285, topicCn: "", answerFr: `De jardiner dans des lieux publics`, answerCn: `在公共场所进行园艺活动` },
          { id: 286, topicCn: "", answerFr: `Les bienfaits de la déconnexion pendant les congés`, answerCn: `休假期间远离网络的好处` },
          { id: 287, topicCn: "", answerFr: `De l’arrivée d’une femme dans un village`, answerCn: `关于一名女子来到一个村庄` },
          { id: 288, topicCn: "", answerFr: `Son humour fait passer un message sérieux`, answerCn: `他的幽默传达了一个严肃的信息` },

          { type: "section", titleCn: "T33", descFr: "", descCn: "" },
          { id: 289, topicCn: "", answerFr: `Aux professeurs qui feront participer leurs élèves`, answerCn: `面向那些会让学生参与进来的老师们` },
          { id: 290, topicCn: "", answerFr: `Elle est bonne pour la santé`, answerCn: `它对健康有益` },
          { id: 291, topicCn: "", answerFr: `Il peut partager sa passion avec un public`, answerCn: `他可以与公众分享自己的热情` },
          { id: 292, topicCn: "", answerFr: `Pour lui proposer des dates de rencontre`, answerCn: `为了给他提议几个见面日期` },
          { id: 293, topicCn: "", answerFr: `Travailler dans une maison d’édition`, answerCn: `在出版社工作` },
          { id: 294, topicCn: "", answerFr: `L’enseignement est d’un bon niveau`, answerCn: `教学水平不错` },
          { id: 295, topicCn: "", answerFr: `Ils commencent plus tôt que d’habitude`, answerCn: `他们比平时开始得更早` },
          { id: 296, topicCn: "", answerFr: `Les conséquences du travail de nuit sur la santé`, answerCn: `夜班工作对健康的后果` },
          { id: 297, topicCn: "", answerFr: `Envoyer un courriel`, answerCn: `发送一封电子邮件` },

          { type: "section", titleCn: "T34", descFr: "", descCn: "" },
          { id: 298, topicCn: "", answerFr: `Écrire un message à monsieur Dubois`, answerCn: `给Dubois先生写一条消息` },
          { id: 299, topicCn: "", answerFr: `Leur forme`, answerCn: `它们的形状` },
          { id: 300, topicCn: "", answerFr: `Favoriser la cohabitation entre les générations`, answerCn: `促进代际之间的共同生活` },
          { id: 301, topicCn: "", answerFr: `Ils donnent accès au sauna`, answerCn: `它们可以进入桑拿房` },
          { id: 302, topicCn: "", answerFr: `Accueillir le théâtre à l’école`, answerCn: `把戏剧引入学校` },
          { id: 303, topicCn: "", answerFr: `Sur une île`, answerCn: `在一座岛上` },
          { id: 304, topicCn: "", answerFr: `On s’en méfie en France`, answerCn: `在法国人们对它持谨慎态度` },
          { id: 305, topicCn: "", answerFr: `Les échanges en famille s’améliorent`, answerCn: `家庭交流有所改善` },
          { id: 306, topicCn: "", answerFr: `Réaliser une étude d’observation des astres`, answerCn: `开展一项天体观测研究` },

          { type: "section", titleCn: "T35", descFr: "", descCn: "" },
          { id: 307, topicCn: "", answerFr: `Enseigner une langue`, answerCn: `教授一门语言` },
          { id: 308, topicCn: "", answerFr: `De devenir membre de l’orchestre municipal`, answerCn: `成为市立乐团的一员` },
          { id: 309, topicCn: "", answerFr: `D’une idée nouvelle de recyclage`, answerCn: `关于一个新的回收理念` },
          { id: 310, topicCn: "", answerFr: `De nouveaux horaires`, answerCn: `新的时间安排` },
          { id: 311, topicCn: "", answerFr: `Obtenir des articles variés`, answerCn: `获得种类多样的文章` },
          { id: 312, topicCn: "", answerFr: `De développer des projets collectifs pour la ville`, answerCn: `为城市发展集体项目` },
          { id: 313, topicCn: "", answerFr: `De visiter une grande exposition`, answerCn: `去参观一个大型展览` },
          { id: 314, topicCn: "", answerFr: `Demander un justificatif`, answerCn: `索要一份证明材料` },
          { id: 315, topicCn: "", answerFr: `Développer la formation continue`, answerCn: `发展继续教育` },

          { type: "section", titleCn: "T36", descFr: "", descCn: "" },
          { id: 316, topicCn: "", answerFr: `Gagner de l’argent pour leur séjour`, answerCn: `赚钱来支付他们的停留费用` },
          { id: 317, topicCn: "", answerFr: `De l’aide pour une association`, answerCn: `给一个协会提供帮助` },
          { id: 318, topicCn: "", answerFr: `Leur rendement au travail diminue`, answerCn: `他们的工作效率下降` },
          { id: 319, topicCn: "", answerFr: `Elles habitent dans le même pays`, answerCn: `她们住在同一个国家` },
          { id: 320, topicCn: "", answerFr: `De se reposer et de découvrir le milieu marin`, answerCn: `去休息并探索海洋环境` },
          { id: 321, topicCn: "", answerFr: `C’est un appui pédagogique supplémentaire`, answerCn: `这是一种额外的教学支持` },
          { id: 322, topicCn: "", answerFr: `Parler à des dessinateurs`, answerCn: `和画家/绘图者交流` },
          { id: 323, topicCn: "", answerFr: `La quête du bonheur facile`, answerCn: `对轻易获得幸福的追求` },
          { id: 324, topicCn: "", answerFr: `Il explique l’idée de départ d’un livre de Modiano`, answerCn: `他解释了一本莫迪亚诺作品最初的构想` },

          { type: "section", titleCn: "T37", descFr: "", descCn: "" },
          { id: 325, topicCn: "", answerFr: `Présenter un film`, answerCn: `介绍一部电影` },
          { id: 326, topicCn: "", answerFr: `De manger quotidiennement du chocolat`, answerCn: `每天吃巧克力` },
          { id: 327, topicCn: "", answerFr: `Annuler son achat`, answerCn: `取消购买` },
          { id: 328, topicCn: "", answerFr: `Les dangers des aliments mal conservés`, answerCn: `保存不当食物的危险` },
          { id: 329, topicCn: "", answerFr: `Pour faire des économies de papier`, answerCn: `为了节省纸张` },
          { id: 330, topicCn: "", answerFr: `Améliorer l’environnement professionnel`, answerCn: `改善职业环境` },
          { id: 331, topicCn: "", answerFr: `Les frais d’envoi peuvent en augmenter le coût`, answerCn: `运费可能会提高其成本` },
          { id: 332, topicCn: "", answerFr: `Un jeu`, answerCn: `一个游戏` },
          { id: 333, topicCn: "", answerFr: `Elle est sous-estimée en tant que moyen d’amélioration`, answerCn: `它作为一种改进手段被低估了` },

          { type: "section", titleCn: "T38", descFr: "", descCn: "" },
          { id: 334, topicCn: "", answerFr: `De dormir au milieu de la nature`, answerCn: `在大自然中睡觉` },
          { id: 335, topicCn: "", answerFr: `Pour éviter de tomber malade`, answerCn: `为了避免生病` },
          { id: 336, topicCn: "", answerFr: `De devenir membre de l’orchestre municipal`, answerCn: `成为市立乐团的一员` },
          { id: 337, topicCn: "", answerFr: `Assister à des spectacles`, answerCn: `观看演出` },
          { id: 338, topicCn: "", answerFr: `Des activités de loisir`, answerCn: `一些休闲活动` },
          { id: 339, topicCn: "", answerFr: `Assister à un spectacle`, answerCn: `观看一场演出` },
          { id: 340, topicCn: "", answerFr: `Ils permettent un contact direct avec un écran tactile`, answerCn: `它们可以让人直接接触触摸屏` },
          { id: 341, topicCn: "", answerFr: `Une méthode pour choisir une formation`, answerCn: `一种选择培训的方法` },
          { id: 342, topicCn: "", answerFr: `Le secret d’une bonne préparation`, answerCn: `良好准备的秘诀` },

          { type: "section", titleCn: "T39", descFr: "", descCn: "" },
          { id: 343, topicCn: "", answerFr: `Elle réunit les caractéristiques de deux continents`, answerCn: `它结合了两个大洲的特征` },
          { id: 344, topicCn: "", answerFr: `De faire un don`, answerCn: `进行捐赠` },
          { id: 345, topicCn: "", answerFr: `De libérer les lieux pendant les travaux`, answerCn: `在施工期间腾空场地` },
          { id: 346, topicCn: "", answerFr: `La majorité des solariums ne respectent pas du tout la loi`, answerCn: `大多数日光浴中心完全不遵守法律` },
          { id: 347, topicCn: "", answerFr: `De suivre une formation`, answerCn: `参加培训` },
          { id: 348, topicCn: "", answerFr: `De faire une visite originale`, answerCn: `进行一次别出心裁的参观` },
          { id: 349, topicCn: "", answerFr: `La pression de la société`, answerCn: `社会压力` },
          { id: 350, topicCn: "", answerFr: `Mieux comprendre les préférences alimentaires des enfants`, answerCn: `更好地理解孩子们的饮食偏好` },
          { id: 351, topicCn: "", answerFr: `Promouvoir d’autres offres commerciales de la SNCF`, answerCn: `推广法国国铁的其他商业优惠` },

          { type: "section", titleCn: "T40", descFr: "", descCn: "" },
          { id: 352, topicCn: "", answerFr: `Gagner de l’argent pour leur séjour`, answerCn: `赚钱来支付他们的停留费用` },
          { id: 353, topicCn: "", answerFr: `De participer à un jeu`, answerCn: `参加一个游戏` },
          { id: 354, topicCn: "", answerFr: `De poser leurs jours de vacances`, answerCn: `安排他们的休假天数` },
          { id: 355, topicCn: "", answerFr: `Demander de l’aide`, answerCn: `寻求帮助` },
          { id: 356, topicCn: "", answerFr: `Transporter des personnes`, answerCn: `运送人员` },
          { id: 357, topicCn: "", answerFr: `Il est proche des lieux à visiter`, answerCn: `它靠近可参观的地点` },
          { id: 358, topicCn: "", answerFr: `De traiter seul des affections bénignes`, answerCn: `自行处理一些轻微疾病` },
          { id: 359, topicCn: "", answerFr: `Les personnes qui y travaillent`, answerCn: `在那里工作的人` },
          { id: 360, topicCn: "", answerFr: `Les clients ont fait un mauvais choix lors de l’achat`, answerCn: `顾客在购买时做出了错误选择` },

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
