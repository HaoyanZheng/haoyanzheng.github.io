#!/usr/bin/env python3
import csv
import re
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 [
          { type: "section", titleCn: "T1", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L’attitude des touristes accélère sa dégradation.`, answerCn: `游客的行为加速了它的恶化。` },
          { id: 2, topicCn: "", answerFr: `C’est un temps de découverte et l’humanité.`, answerCn: `这是一个探索与人文体验的时期。` },
          { id: 3, topicCn: "", answerFr: `C’est à la fois un restaurant et une galerie d’art.`, answerCn: `它既是餐厅也是艺术画廊。` },
          { id: 4, topicCn: "", answerFr: `À orienter la recherche en prenant la nature comme modèle.`, answerCn: `以自然为模型来引导研究。` },
          { id: 5, topicCn: "", answerFr: `Ils sont à l’origine de créations d’emplois.`, answerCn: `他们创造了就业机会。` },
          { id: 6, topicCn: "", answerFr: `Ils répondent à ses convictions.`, answerCn: `他们符合他的信念。` },

          { type: "section", titleCn: "T2", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `À créer une échelle lisible de classification des élèves.`, answerCn: `建立一个清晰的学生分类等级。` },
          { id: 2, topicCn: "", answerFr: `Du bon vouloir du client.`, answerCn: `取决于客户的意愿。` },
          { id: 3, topicCn: "", answerFr: `Elle met en danger le marché du travail.`, answerCn: `它威胁就业市场。` },
          { id: 4, topicCn: "", answerFr: `Les comportements machistes perdurent dans l’univers sportif.`, answerCn: `体育界仍然存在大男子主义行为。` },
          { id: 5, topicCn: "", answerFr: `Un aménagement territorial en fonction des données météorologiques.`, answerCn: `根据气象数据进行国土规划。` },
          { id: 6, topicCn: "", answerFr: `De l’absurdité qu’il y a valorisé leur manque de culture scientifique.`, answerCn: `讽刺地赞扬他们科学文化的缺乏。` },

          { type: "section", titleCn: "T3", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La tenue vestimentaire influence l’état psychologique.`, answerCn: `穿着会影响心理状态。` },
          { id: 2, topicCn: "", answerFr: `Ils sont tentés par les dépenses.`, answerCn: `他们容易被消费诱惑。` },
          { id: 3, topicCn: "", answerFr: `L’aspect magique de la métamorphose de la matière.`, answerCn: `物质变化的神奇特性。` },
          { id: 4, topicCn: "", answerFr: `Donner des conseils de préparation.`, answerCn: `提供准备建议。` },
          { id: 5, topicCn: "", answerFr: `Le besoin de ressembler aux autres.`, answerCn: `想与他人相似的需求。` },
          { id: 6, topicCn: "", answerFr: `La qualité croissante des résultats.`, answerCn: `结果质量不断提高。` },

          { type: "section", titleCn: "T4", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L’absence de formation sur l’élaboration d’un budget.`, answerCn: `缺乏预算制定培训。` },
          { id: 2, topicCn: "", answerFr: `Elles ont été revendues.`, answerCn: `它们被转卖了。` },
          { id: 3, topicCn: "", answerFr: `En observant divers types d’interlocuteurs.`, answerCn: `通过观察不同类型的谈话对象。` },
          { id: 4, topicCn: "", answerFr: `Le paradoxe : elle expose une absence d’œuvres.`, answerCn: `悖论：它展示的是没有作品。` },
          { id: 5, topicCn: "", answerFr: `Il met en doute l’interprétation des résultats.`, answerCn: `他质疑对结果的解释。` },
          { id: 6, topicCn: "", answerFr: `C’est un symbole fort de cette province.`, answerCn: `这是这个省的重要象征。` },

          { type: "section", titleCn: "T5", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `À créer une échelle lisible de classification des élèves.`, answerCn: `建立清晰的学生分类等级。` },
          { id: 2, topicCn: "", answerFr: `Manger plus léger sans changer ses habitudes.`, answerCn: `不改变习惯而吃得更清淡。` },
          { id: 3, topicCn: "", answerFr: `La mise en relief des formules figées de la langue.`, answerCn: `突出语言中的固定表达。` },
          { id: 4, topicCn: "", answerFr: `Déterminer les nouveaux enjeux du théâtre.`, answerCn: `确定戏剧的新议题。` },
          { id: 5, topicCn: "", answerFr: `De prendre ouvertement position dans des rivalités internes.`, answerCn: `在内部竞争中公开表态。` },
          { id: 6, topicCn: "", answerFr: `Des circuits de distribution courts.`, answerCn: `短供应链。` },

          { type: "section", titleCn: "T6", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `D’un appel à projets imaginaires.`, answerCn: `来自一个虚构项目征集。` },
          { id: 2, topicCn: "", answerFr: `D’une histoire familiale.`, answerCn: `来自一个家庭故事。` },
          { id: 3, topicCn: "", answerFr: `Ils nagent en plein air dans la capitale.`, answerCn: `他们在首都的露天游泳。` },
          { id: 4, topicCn: "", answerFr: `De la reprise d’une œuvre.`, answerCn: `对一部作品的再创作。` },
          { id: 5, topicCn: "", answerFr: `Ils sont à l’origine de créations d’emplois.`, answerCn: `他们创造了就业。` },
          { id: 6, topicCn: "", answerFr: `Il considère que le phénomène doit être analysé.`, answerCn: `他认为这个现象需要分析。` },

          { type: "section", titleCn: "T7", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il contrôle rigoureusement toutes les formalités de garantie.`, answerCn: `他严格检查所有保修手续。` },
          { id: 2, topicCn: "", answerFr: `La tenue vestimentaire influence l’état psychologique.`, answerCn: `穿着会影响心理状态。` },
          { id: 3, topicCn: "", answerFr: `Elle offre une expérience à un public de tous âges.`, answerCn: `它为各年龄群提供体验。` },
          { id: 4, topicCn: "", answerFr: `L’assujettissement insidieux des mineurs.`, answerCn: `未成年人被隐性控制。` },
          { id: 5, topicCn: "", answerFr: `Une modernisation des procédures d’emprunt des documents.`, answerCn: `借阅流程现代化。` },
          { id: 6, topicCn: "", answerFr: `Elle crée des besoins pour réutiliser de vieux remèdes.`, answerCn: `它创造需求以重新使用旧药方。` },

          { type: "section", titleCn: "T8", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un service de livraison express du courrier.`, answerCn: `一种快递邮件服务。` },
          { id: 2, topicCn: "", answerFr: `C’est un temps de découverte et d’humanité.`, answerCn: `这是探索与人文体验的时刻。` },
          { id: 3, topicCn: "", answerFr: `Elles appuient leur gestion sur la concertation.`, answerCn: `她们通过协商来进行管理。` },
          { id: 4, topicCn: "", answerFr: `Les discussions s’annoncent longues et difficiles.`, answerCn: `讨论将会漫长而困难。` },
          { id: 5, topicCn: "", answerFr: `Inciter les usagers à pratiquer d’autres modes de déplacement.`, answerCn: `鼓励人们使用其他交通方式。` },
          { id: 6, topicCn: "", answerFr: `Trouver des solutions aux difficultés quotidiennes.`, answerCn: `寻找日常困难的解决办法。` },

          { type: "section", titleCn: "T9", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un service de livraison express du courrier.`, answerCn: `一种快递邮件服务。` },
          { id: 2, topicCn: "", answerFr: `Elles ont été revendues.`, answerCn: `它们被转卖。` },
          { id: 3, topicCn: "", answerFr: `Les responsables de petites entreprises.`, answerCn: `小企业负责人。` },
          { id: 4, topicCn: "", answerFr: `Comme le reflet d’un caractère authentique.`, answerCn: `作为真实个性的体现。` },
          { id: 5, topicCn: "", answerFr: `Ils prennent en considération le facteur social.`, answerCn: `他们考虑社会因素。` },
          { id: 6, topicCn: "", answerFr: `La violence est indépendante de la densité humaine.`, answerCn: `暴力与人口密度无关。` },

          { type: "section", titleCn: "T10", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Pour s’acheter une maison.`, answerCn: `为了买房。` },
          { id: 2, topicCn: "", answerFr: `Montrer la variété de la langue française.`, answerCn: `展示法语的多样性。` },
          { id: 3, topicCn: "", answerFr: `Laisser l’élève progresser à son rythme en l’accompagnant patiemment.`, answerCn: `耐心陪伴学生按自己的节奏进步。` },
          { id: 4, topicCn: "", answerFr: `Contrôler l’aptitude à la conduite d’une certaine catégorie d’usagers.`, answerCn: `检查某类用户的驾驶能力。` },
          { id: 5, topicCn: "", answerFr: `Exploiter différemment les terres endommagées.`, answerCn: `以不同方式利用受损土地。` },
          { id: 6, topicCn: "", answerFr: `C’est un symbole fort de cette province.`, answerCn: `这是该省的重要象征。` },

          { type: "section", titleCn: "T11", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a besoin d’être perfectionné.`, answerCn: `它需要进一步完善。` },
          { id: 2, topicCn: "", answerFr: `Elle confirme une théorie ancienne.`, answerCn: `它证实了一个古老的理论。` },
          { id: 3, topicCn: "", answerFr: `Elle est dans l’innovation constante.`, answerCn: `它处于持续创新之中。` },
          { id: 4, topicCn: "", answerFr: `Elle représente une solution d’avenir.`, answerCn: `它代表一种未来的解决方案。` },
          { id: 5, topicCn: "", answerFr: `Pour conserver la trace du patrimoine architectural.`, answerCn: `为了保留建筑遗产的痕迹。` },
          { id: 6, topicCn: "", answerFr: `Ils programment les mêmes musiciens.`, answerCn: `他们安排同样的音乐家演出。` },

          { type: "section", titleCn: "T12", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il permet d’entrer en relation avec les autres.`, answerCn: `它能让人与他人建立联系。` },
          { id: 2, topicCn: "", answerFr: `La question est préoccupante pour les plus jeunes.`, answerCn: `这个问题让年轻人担忧。` },
          { id: 3, topicCn: "", answerFr: `Le manque d’estime de soi.`, answerCn: `缺乏自信。` },
          { id: 4, topicCn: "", answerFr: `En s’engageant comme citoyenne.`, answerCn: `通过以公民身份参与。` },
          { id: 5, topicCn: "", answerFr: `La filière aquacole fragilise l’équilibre alimentaire mondial.`, answerCn: `水产养殖产业削弱全球粮食平衡。` },
          { id: 6, topicCn: "", answerFr: `La perte de son emploi.`, answerCn: `失去工作。` },

          { type: "section", titleCn: "T13", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un album de souvenirs personnels.`, answerCn: `一本个人回忆相册。` },
          { id: 2, topicCn: "", answerFr: `La surabondance de sollicitations.`, answerCn: `过多的请求与干扰。` },
          { id: 3, topicCn: "", answerFr: `Ils nagent en plein air dans la capitale.`, answerCn: `他们在首都的露天游泳。` },
          { id: 4, topicCn: "", answerFr: `Parce qu’elle connaît la discipline dont il faut faire preuve pour bien jouer.`, answerCn: `因为她知道要演奏好需要严格的训练。` },
          { id: 5, topicCn: "", answerFr: `Une optimisation du confort auditif par des sons personnalisables.`, answerCn: `通过个性化声音优化听觉体验。` },
          { id: 6, topicCn: "", answerFr: `La perte de sa liberté intellectuelle.`, answerCn: `失去思想自由。` },

          { type: "section", titleCn: "T14", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il y a eu une panne d’électricité dans le métro.`, answerCn: `地铁发生了停电。` },
          { id: 2, topicCn: "", answerFr: `Il rappelle à l’ordre un employé.`, answerCn: `他警告了一名员工。` },
          { id: 3, topicCn: "", answerFr: `L’essor du travail féminin.`, answerCn: `女性就业的增长。` },
          { id: 4, topicCn: "", answerFr: `Les jeunes diplômés privilégient le travail en milieu urbain.`, answerCn: `年轻毕业生更倾向在城市工作。` },
          { id: 5, topicCn: "", answerFr: `Promouvoir la campagne comme destination touristique.`, answerCn: `推广乡村作为旅游目的地。` },
          { id: 6, topicCn: "", answerFr: `Des professionnels de santé et des utilisateurs vérifient les notices.`, answerCn: `医疗专业人员和用户检查说明书。` },

          { type: "section", titleCn: "T15", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `D’un appel à projets imaginaires.`, answerCn: `来自虚构项目征集。` },
          { id: 2, topicCn: "", answerFr: `Elle confirme une théorie ancienne.`, answerCn: `它证实了一个古老理论。` },
          { id: 3, topicCn: "", answerFr: `Les discussions s’annoncent longues et difficiles.`, answerCn: `讨论将会漫长而困难。` },
          { id: 4, topicCn: "", answerFr: `C’est à la fois un restaurant et une galerie d’art.`, answerCn: `它既是餐厅也是艺术画廊。` },
          { id: 5, topicCn: "", answerFr: `Une littérature portée sur l’interdisciplinarité.`, answerCn: `一种强调跨学科的文学。` },
          { id: 6, topicCn: "", answerFr: `Optimiser l’utilisation des appareils.`, answerCn: `优化设备使用。` },

          { type: "section", titleCn: "T16", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il permet d’entrer en relation avec les autres.`, answerCn: `它能让人与他人建立联系。` },
          { id: 2, topicCn: "", answerFr: `De sorties originales.`, answerCn: `一些独特的外出活动。` },
          { id: 3, topicCn: "", answerFr: `De côtoyer des coutumes différentes.`, answerCn: `接触不同的风俗。` },
          { id: 4, topicCn: "", answerFr: `Ils sont à l’origine de créations d’emplois.`, answerCn: `他们创造了就业机会。` },
          { id: 5, topicCn: "", answerFr: `La filière aquacole fragilise l’équilibre alimentaire mondial.`, answerCn: `水产养殖产业削弱全球粮食平衡。` },
          { id: 6, topicCn: "", answerFr: `Établir des priorités s’avère être très difficile.`, answerCn: `确定优先事项非常困难。` },

          { type: "section", titleCn: "T17", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Du bon vouloir du client.`, answerCn: `取决于客户的意愿。` },
          { id: 2, topicCn: "", answerFr: `Elle confirme une théorie ancienne.`, answerCn: `它证实了一个古老理论。` },
          { id: 3, topicCn: "", answerFr: `Il a intégré l’étude de la presse à ses programmes.`, answerCn: `他把媒体研究纳入课程。` },
          { id: 4, topicCn: "", answerFr: `Des recettes ont été baptisées en l’honneur de clients réputés.`, answerCn: `一些菜肴以知名顾客命名。` },
          { id: 5, topicCn: "", answerFr: `Elle s’applique très rarement au travail.`, answerCn: `她很少认真工作。` },
          { id: 6, topicCn: "", answerFr: `De l’absurdité qu’il y a à valoriser leur manque de culture scientifique.`, answerCn: `讽刺地赞扬他们缺乏科学文化。` },

          { type: "section", titleCn: "T18", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils sont encouragés lors de leur apprentissage.`, answerCn: `他们在学习过程中受到鼓励。` },
          { id: 2, topicCn: "", answerFr: `À la difficulté de se retrouver dans un même lieu.`, answerCn: `很难在同一地点相聚。` },
          { id: 3, topicCn: "", answerFr: `Il a intégré l’étude de la presse à ses programmes.`, answerCn: `他把媒体研究纳入课程。` },
          { id: 4, topicCn: "", answerFr: `Elle cherche à privilégier le travail avec des entreprises françaises.`, answerCn: `她希望优先与法国企业合作。` },
          { id: 5, topicCn: "", answerFr: `Elle crée des besoins pour réutiliser de vieux remèdes.`, answerCn: `它创造需求以重新利用旧疗法。` },
          { id: 6, topicCn: "", answerFr: `Elle critique la fiabilité des méthodes d’investigation utilisées.`, answerCn: `她批评所用调查方法的可靠性。` },

          { type: "section", titleCn: "T19", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un album de souvenirs personnels.`, answerCn: `一本个人回忆相册。` },
          { id: 2, topicCn: "", answerFr: `Journaliste.`, answerCn: `记者。` },
          { id: 3, topicCn: "", answerFr: `En observant divers types d’interlocuteurs.`, answerCn: `通过观察不同类型的谈话对象。` },
          { id: 4, topicCn: "", answerFr: `Sur l’utilisation des recettes fiscales pour régler la dette.`, answerCn: `通过税收收入解决债务问题。` },
          { id: 5, topicCn: "", answerFr: `La qualité croissante des résultats.`, answerCn: `结果质量不断提高。` },
          { id: 6, topicCn: "", answerFr: `La construction d’un édifice emblématique.`, answerCn: `建造一个标志性建筑。` },

          { type: "section", titleCn: "T20", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Obtenir un statut professionnel officiel pour les biffins.`, answerCn: `为拾荒者获得正式职业身份。` },
          { id: 2, topicCn: "", answerFr: `La question est préoccupante pour les plus jeunes.`, answerCn: `这个问题让年轻人担忧。` },
          { id: 3, topicCn: "", answerFr: `Les jeunes diplômés privilégient le travail en milieu urbain.`, answerCn: `年轻毕业生更倾向城市工作。` },
          { id: 4, topicCn: "", answerFr: `Les pratiques de pêcheurs.`, answerCn: `渔民的做法。` },
          { id: 5, topicCn: "", answerFr: `La seule visée de cet enseignement est d’initier les enfants à la langue.`, answerCn: `该教学的唯一目的就是让孩子入门语言。` },
          { id: 6, topicCn: "", answerFr: `Elle est encadrée par des normes strictes.`, answerCn: `它受到严格规范的监管。` },

          { type: "section", titleCn: "T21", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Adopter un mode de vie collectif responsable.`, answerCn: `采取一种负责任的集体生活方式。` },
          { id: 2, topicCn: "", answerFr: `D’un appel à projets imaginaires.`, answerCn: `来自一个虚构项目征集。` },
          { id: 3, topicCn: "", answerFr: `Elle est dans l’innovation constante.`, answerCn: `它处于持续创新之中。` },
          { id: 4, topicCn: "", answerFr: `Donner des conseils de préparation.`, answerCn: `提供准备建议。` },
          { id: 5, topicCn: "", answerFr: `Elle enrichit les rapports humains.`, answerCn: `它丰富了人与人之间的关系。` },
          { id: 6, topicCn: "", answerFr: `La qualité croissante des résultats.`, answerCn: `结果质量不断提高。` },

          { type: "section", titleCn: "T22", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Établir un certificat médical.`, answerCn: `开具医疗证明。` },
          { id: 2, topicCn: "", answerFr: `L’absence de formation sur l’élaboration d’un budget.`, answerCn: `缺乏预算制定培训。` },
          { id: 3, topicCn: "", answerFr: `Elles permettent à la société de fonctionner.`, answerCn: `它们使社会能够运转。` },
          { id: 4, topicCn: "", answerFr: `Le temps nécessaire pour découvrir la cachette.`, answerCn: `找到藏匿地点所需的时间。` },
          { id: 5, topicCn: "", answerFr: `Leur manque d’investissement dans des actions à caractère social.`, answerCn: `他们在社会活动方面投入不足。` },
          { id: 6, topicCn: "", answerFr: `L’intérêt principal de sa mise en place a disparu.`, answerCn: `设立它的主要意义已经消失。` },

          { type: "section", titleCn: "T23", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il contrôle rigoureusement toutes les formalités de garantie.`, answerCn: `他严格检查所有保修手续。` },
          { id: 2, topicCn: "", answerFr: `Montrer la variété de la langue française.`, answerCn: `展示法语的多样性。` },
          { id: 3, topicCn: "", answerFr: `Il enrichit les relations humaines.`, answerCn: `它丰富了人与人之间的关系。` },
          { id: 4, topicCn: "", answerFr: `Ses lecteurs sont encouragés à réfléchir.`, answerCn: `读者被鼓励去思考。` },
          { id: 5, topicCn: "", answerFr: `De permettre aux jeunes de parler de leur chagrin.`, answerCn: `让年轻人表达他们的悲伤。` },
          { id: 6, topicCn: "", answerFr: `De l’absurdité qu’il y a à valoriser leur manque de culture scientifique.`, answerCn: `讽刺地赞扬他们缺乏科学文化。` },

          { type: "section", titleCn: "T24", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il permet d’entrer en relation avec les autres.`, answerCn: `它让人与他人建立联系。` },
          { id: 2, topicCn: "", answerFr: `La question est préoccupante pour les plus jeunes.`, answerCn: `这个问题让年轻人担忧。` },
          { id: 3, topicCn: "", answerFr: `Le manque d’estime de soi.`, answerCn: `缺乏自信。` },
          { id: 4, topicCn: "", answerFr: `Pour conserver la trace du patrimoine architectural.`, answerCn: `为了保留建筑遗产的痕迹。` },
          { id: 5, topicCn: "", answerFr: `Ils sont à l’origine de créations d’emplois.`, answerCn: `他们创造了就业机会。` },
          { id: 6, topicCn: "", answerFr: `La perte de sa liberté intellectuelle.`, answerCn: `失去思想自由。` },

          { type: "section", titleCn: "T25", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `D’un appel à projets imaginaires.`, answerCn: `来自虚构项目征集。` },
          { id: 2, topicCn: "", answerFr: `D’une histoire familiale.`, answerCn: `来自一个家庭故事。` },
          { id: 3, topicCn: "", answerFr: `Ils nagent en plein air dans la capitale.`, answerCn: `他们在首都露天游泳。` },
          { id: 4, topicCn: "", answerFr: `Sur l’utilisation des recettes fiscales pour régler la dette.`, answerCn: `利用税收收入解决债务。` },
          { id: 5, topicCn: "", answerFr: `Exercer une activité intellectuellement enrichissante.`, answerCn: `从事富有思想意义的活动。` },
          { id: 6, topicCn: "", answerFr: `De rejeter les résultats des dernières recherches.`, answerCn: `否定最新研究成果。` },

          { type: "section", titleCn: "T26", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Du bon vouloir du client.`, answerCn: `取决于客户意愿。` },
          { id: 2, topicCn: "", answerFr: `Elle confirme une théorie ancienne.`, answerCn: `它证实了一个古老理论。` },
          { id: 3, topicCn: "", answerFr: `Il enrichit les relations humaines.`, answerCn: `它丰富人与人之间关系。` },
          { id: 4, topicCn: "", answerFr: `En s’engageant comme citoyenne.`, answerCn: `通过以公民身份参与。` },
          { id: 5, topicCn: "", answerFr: `L’intérêt de partager des services.`, answerCn: `共享服务的好处。` },
          { id: 6, topicCn: "", answerFr: `Les interventions nécessaires des États dans l’économie.`, answerCn: `国家在经济中的必要干预。` },

          { type: "section", titleCn: "T27", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Accompagner les clients dans une démarche d’achat responsable.`, answerCn: `陪伴客户进行负责任消费。` },
          { id: 2, topicCn: "", answerFr: `La surabondance de sollicitations.`, answerCn: `过多的请求与干扰。` },
          { id: 3, topicCn: "", answerFr: `Les discussions s’annoncent longues et difficiles.`, answerCn: `讨论将会漫长而困难。` },
          { id: 4, topicCn: "", answerFr: `Elle offre des postes épanouissants quoique peu rémunérateurs.`, answerCn: `它提供充实但收入不高的职位。` },
          { id: 5, topicCn: "", answerFr: `Elle permet de faire évoluer le regard des jeunes sur l’école.`, answerCn: `它改变年轻人对学校的看法。` },
          { id: 6, topicCn: "", answerFr: `Les habitants sont indifférents à l’une des richesses du Québec.`, answerCn: `居民对魁北克的一项财富漠不关心。` },

          { type: "section", titleCn: "T28", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Journaliste.`, answerCn: `记者。` },
          { id: 2, topicCn: "", answerFr: `Étudier les trajectoires des déchets cosmiques.`, answerCn: `研究太空垃圾轨道。` },
          { id: 3, topicCn: "", answerFr: `Le manque d’estime de soi.`, answerCn: `缺乏自信。` },
          { id: 4, topicCn: "", answerFr: `Elle possède un nom inapproprié.`, answerCn: `它有一个不恰当的名字。` },
          { id: 5, topicCn: "", answerFr: `Sa clientèle s’est diversifiée.`, answerCn: `它的客户群多样化。` },
          { id: 6, topicCn: "", answerFr: `C’est un symbole fort de cette province.`, answerCn: `这是该省的重要象征。` },

          { type: "section", titleCn: "T29", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `D’organiser des repas collectifs dans un lieu inhabituel.`, answerCn: `在非常规地点组织集体用餐。` },
          { id: 2, topicCn: "", answerFr: `Étudier les trajectoires des déchets cosmiques.`, answerCn: `研究太空垃圾轨道。` },
          { id: 3, topicCn: "", answerFr: `Le français a trouvé sa place au carrefour du pluralisme linguistique.`, answerCn: `法语在多语言环境中找到了位置。` },
          { id: 4, topicCn: "", answerFr: `Les jeunes diplômés privilégient le travail en milieu urbain.`, answerCn: `年轻毕业生更倾向城市工作。` },
          { id: 5, topicCn: "", answerFr: `La qualité croissante des résultats.`, answerCn: `结果质量不断提高。` },
          { id: 6, topicCn: "", answerFr: `On multiplie l’utilisation de parfums artificiels.`, answerCn: `人工香料的使用增加。` },

          { type: "section", titleCn: "T30", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L’absence de formation sur l’élaboration d’un budget.`, answerCn: `缺乏预算制定培训。` },
          { id: 2, topicCn: "", answerFr: `L’attitude des touristes accélère sa dégradation.`, answerCn: `游客行为加速其恶化。` },
          { id: 3, topicCn: "", answerFr: `Elle peut rompre les branches.`, answerCn: `它可能折断树枝。` },
          { id: 4, topicCn: "", answerFr: `Ils nagent en plein air dans la capitale.`, answerCn: `他们在首都露天游泳。` },
          { id: 5, topicCn: "", answerFr: `De la reprise d’une œuvre.`, answerCn: `对一部作品的再创作。` },
          { id: 6, topicCn: "", answerFr: `Pour conserver la trace du patrimoine architectural.`, answerCn: `为了保存建筑遗产痕迹。` },

          { type: "section", titleCn: "T31", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il bavarde régulièrement avec son voisin anglais.`, answerCn: `他经常和他的英国邻居聊天。` },
          { id: 2, topicCn: "", answerFr: `La surabondance de sollicitations.`, answerCn: `过多的请求与干扰。` },
          { id: 3, topicCn: "", answerFr: `De prendre part à des expéditions scientifiques.`, answerCn: `参与科学探险。` },
          { id: 4, topicCn: "", answerFr: `Pour s’imprégner des rencontres effectuées.`, answerCn: `为了吸收与他人交流的体验。` },
          { id: 5, topicCn: "", answerFr: `Exercer une activité intellectuellement enrichissante.`, answerCn: `从事富有思想意义的活动。` },
          { id: 6, topicCn: "", answerFr: `Une interprétation sincère.`, answerCn: `一种真诚的诠释。` },

          { type: "section", titleCn: "T32", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle l’a laissée complètement indifférente.`, answerCn: `这件事让她完全无动于衷。` },
          { id: 2, topicCn: "", answerFr: `D’une histoire familiale.`, answerCn: `来自一个家庭故事。` },
          { id: 3, topicCn: "", answerFr: `C’est à la fois un restaurant et une galerie d’art.`, answerCn: `它既是餐厅也是艺术画廊。` },
          { id: 4, topicCn: "", answerFr: `La traduction était partielle.`, answerCn: `翻译是不完整的。` },
          { id: 5, topicCn: "", answerFr: `La perte de sa liberté intellectuelle.`, answerCn: `失去思想自由。` },
          { id: 6, topicCn: "", answerFr: `Il a été découvert en Amérique avant d’être introduit en France.`, answerCn: `它先在美洲被发现，之后才传入法国。` },

          { type: "section", titleCn: "T33", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a besoin d’être perfectionné.`, answerCn: `它需要进一步完善。` },
          { id: 2, topicCn: "", answerFr: `La tenue vestimentaire influence l’état psychologique.`, answerCn: `穿着会影响心理状态。` },
          { id: 3, topicCn: "", answerFr: `Les discussions s’annoncent longues et difficiles.`, answerCn: `讨论将会漫长而困难。` },
          { id: 4, topicCn: "", answerFr: `Sur l’utilisation des recettes fiscales pour régler la dette.`, answerCn: `利用税收收入解决债务。` },
          { id: 5, topicCn: "", answerFr: `Une optimisation du confort auditif par des sons personnalisables.`, answerCn: `通过个性化声音优化听觉体验。` },
          { id: 6, topicCn: "", answerFr: `La violence est indépendante de la densité humaine.`, answerCn: `暴力与人口密度无关。` },

          { type: "section", titleCn: "T34", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il a besoin d’être perfectionné.`, answerCn: `它需要进一步完善。` },
          { id: 2, topicCn: "", answerFr: `Étudier les trajectoires des déchets cosmiques.`, answerCn: `研究太空垃圾轨道。` },
          { id: 3, topicCn: "", answerFr: `Le manque d’estime de soi.`, answerCn: `缺乏自信。` },
          { id: 4, topicCn: "", answerFr: `Comme le reflet d’un caractère authentique.`, answerCn: `作为真实个性的体现。` },
          { id: 5, topicCn: "", answerFr: `Ils prennent en considération le facteur social.`, answerCn: `他们考虑社会因素。` },
          { id: 6, topicCn: "", answerFr: `La violence est indépendante de la densité humaine.`, answerCn: `暴力与人口密度无关。` },

          { type: "section", titleCn: "T35", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils sont tentés par les dépenses.`, answerCn: `他们容易被消费诱惑。` },
          { id: 2, topicCn: "", answerFr: `Il préfère intervenir après la fin du match.`, answerCn: `他更愿意在比赛结束后介入。` },
          { id: 3, topicCn: "", answerFr: `Les copies gratuites de fichiers musicaux sur Internet.`, answerCn: `互联网上免费的音乐文件复制。` },
          { id: 4, topicCn: "", answerFr: `Il a des répercussions jusque dans le quotidien des Québécois.`, answerCn: `它甚至影响魁北克人的日常生活。` },
          { id: 5, topicCn: "", answerFr: `Ils émettent quelques réserves sur leur intégration.`, answerCn: `他们对融入提出一些保留意见。` },
          { id: 6, topicCn: "", answerFr: `Les habitants sont indifférents à l’une des richesses du Québec.`, answerCn: `居民对魁北克的一项财富漠不关心。` },

          { type: "section", titleCn: "T36", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il permet d’entrer en relation avec les autres.`, answerCn: `它让人与他人建立联系。` },
          { id: 2, topicCn: "", answerFr: `Les auditeurs ont participé à l’émission.`, answerCn: `听众参与了节目。` },
          { id: 3, topicCn: "", answerFr: `La capacité à révéler une certaine vérité.`, answerCn: `揭示某种真相的能力。` },
          { id: 4, topicCn: "", answerFr: `Elle est dans l’innovation constante.`, answerCn: `它处于持续创新之中。` },
          { id: 5, topicCn: "", answerFr: `Un programme d’éducation pour les jeunes.`, answerCn: `一个面向青少年的教育项目。` },
          { id: 6, topicCn: "", answerFr: `La filière aquacole fragilise l’équilibre alimentaire mondial.`, answerCn: `水产养殖产业削弱全球粮食平衡。` },

          { type: "section", titleCn: "T37", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `De maigrir plus rapidement.`, answerCn: `更快减肥。` },
          { id: 2, topicCn: "", answerFr: `La portée socio-environnementale.`, answerCn: `社会与环境层面的影响。` },
          { id: 3, topicCn: "", answerFr: `Raconter un épisode sentimental de sa propre vie.`, answerCn: `讲述自己生活中的情感经历。` },
          { id: 4, topicCn: "", answerFr: `Définir des politiques pour tenter de les enrayer.`, answerCn: `制定政策试图遏制它们。` },
          { id: 5, topicCn: "", answerFr: `Établir des priorités s’avère très difficile.`, answerCn: `确定优先事项非常困难。` },
          { id: 6, topicCn: "", answerFr: `Aider à une réflexion sur l’existence.`, answerCn: `帮助人们思考人生。` },

          { type: "section", titleCn: "T38", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La découverte de sa fragilité en tant qu’être humain.`, answerCn: `发现作为人类自身的脆弱。` },
          { id: 2, topicCn: "", answerFr: `Elle confirme une théorie ancienne.`, answerCn: `它证实了一个古老理论。` },
          { id: 3, topicCn: "", answerFr: `Le père doit construire la relation au plus tôt sans se cantonner à un seul rôle.`, answerCn: `父亲应尽早建立关系而不仅限于一个角色。` },
          { id: 4, topicCn: "", answerFr: `Une simple plaisanterie.`, answerCn: `一个简单的玩笑。` },
          { id: 5, topicCn: "", answerFr: `Les pièces de qualité.`, answerCn: `高质量的零件。` },
          { id: 6, topicCn: "", answerFr: `Elle s’adapte aux variations climatiques.`, answerCn: `它适应气候变化。` },

          { type: "section", titleCn: "T39", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il rencontrait des difficultés avec les enseignants.`, answerCn: `他与老师相处有困难。` },
          { id: 2, topicCn: "", answerFr: `Elle confirme une théorie ancienne.`, answerCn: `它证实了一个古老理论。` },
          { id: 3, topicCn: "", answerFr: `L’essor du travail féminin.`, answerCn: `女性就业的增长。` },
          { id: 4, topicCn: "", answerFr: `De côtoyer des us et coutumes différents.`, answerCn: `接触不同的风俗习惯。` },
          { id: 5, topicCn: "", answerFr: `Elles les incitent à venir butiner.`, answerCn: `它们吸引蜜蜂前来采蜜。` },
          { id: 6, topicCn: "", answerFr: `Un aménagement territorial en fonction des données météorologiques.`, answerCn: `根据气象数据进行国土规划。` },

          { type: "section", titleCn: "T40", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils sont tentés par les dépenses.`, answerCn: `他们容易被消费诱惑。` },
          { id: 2, topicCn: "", answerFr: `Il préfère intervenir après la fin du match.`, answerCn: `他更愿意在比赛结束后介入。` },
          { id: 3, topicCn: "", answerFr: `Les copies gratuites sur Internet.`, answerCn: `互联网上的免费复制。` },
          { id: 4, topicCn: "", answerFr: `Il peut être complètement évité si on agit maintenant.`, answerCn: `如果现在行动可以完全避免。` },
          { id: 5, topicCn: "", answerFr: `Ils ont un souci de l’intégration.`, answerCn: `他们关心融入问题。` },
          { id: 6, topicCn: "", answerFr: `Problème de communication, aucun moyen de sensibiliser les écologistes.`, answerCn: `沟通问题，没有办法说服环保人士。` },

          { type: "section", titleCn: "新题", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `On met rarement en avant tous les domaines concernés.`, answerCn: `人们很少把所有相关领域都突出展示出来。` },
          { id: 2, topicCn: "", answerFr: `Le manque d’esprit critique des médias.`, answerCn: `媒体缺乏批判性思维。` },
          { id: 3, topicCn: "", answerFr: `La perte d’emplois liée à la disparition des cafés.`, answerCn: `咖啡馆消失导致的就业岗位减少。` },
        ];

"""

# ---- Config ----
TACHE = 3                 # set 1/2/3/etc.
KIND  = "a"               # "a" for answers
OUT_CSV = Path("assets/tcfcaCO/t3.csv")
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
