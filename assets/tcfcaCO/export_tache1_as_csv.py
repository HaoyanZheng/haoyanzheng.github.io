#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 return [
          { type: "section", titleCn: "T1", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La communication avec ses clients.`, answerCn: `与客户沟通。` },
          { id: 2, topicCn: "", answerFr: `De cinéma.`, answerCn: `关于电影。` },
          { id: 3, topicCn: "", answerFr: `Pour modifier une commande.`, answerCn: `为了修改订单。` },
          { id: 4, topicCn: "", answerFr: `L’annulation d’un cours.`, answerCn: `课程取消。` },
          { id: 5, topicCn: "", answerFr: `Elle passe ses congés dans la région.`, answerCn: `她在本地区度假。` },
          { id: 6, topicCn: "", answerFr: `Le contact avec les élèves.`, answerCn: `与学生的接触。` },
          { id: 7, topicCn: "", answerFr: `Vérifier si un courrier est bien arrivé.`, answerCn: `确认邮件是否已到达。` },
          { id: 8, topicCn: "", answerFr: `Les difficultés en cas d’échange.`, answerCn: `交换时的困难。` },
          { id: 9, topicCn: "", answerFr: `Les conditions de recrutement sont plus difficiles aujourd’hui.`, answerCn: `如今招聘条件更困难。` },

          { type: "section", titleCn: "T2", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il est tombé dans son escalier.`, answerCn: `他在楼梯上摔倒了。` },
          { id: 2, topicCn: "", answerFr: `De vivre chez quelqu’un.`, answerCn: `住在别人家里。` },
          { id: 3, topicCn: "", answerFr: `Du dernier film qu’elles ont vu.`, answerCn: `她们最近看的电影。` },
          { id: 4, topicCn: "", answerFr: `Créer occasion de se retrouver en famille.`, answerCn: `创造家庭团聚的机会。` },
          { id: 5, topicCn: "", answerFr: `Remettre un vêtement au vestiaire.`, answerCn: `把衣服放在衣帽间。` },
          { id: 6, topicCn: "", answerFr: `D’essayer un vêtement près du corps.`, answerCn: `试穿贴身衣服。` },
          { id: 7, topicCn: "", answerFr: `À un décorateur.`, answerCn: `找一位室内设计师。` },
          { id: 8, topicCn: "", answerFr: `De déjeuner ensemble.`, answerCn: `一起吃午饭。` },
          { id: 9, topicCn: "", answerFr: `Pratiquer régulièrement un sport.`, answerCn: `定期运动。` },

          { type: "section", titleCn: "T3", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle est située dans une rue bruyante.`, answerCn: `它位于一条嘈杂的街道。` },
          { id: 2, topicCn: "", answerFr: `Il a été très agréablement surpris.`, answerCn: `他感到非常惊喜。` },
          { id: 3, topicCn: "", answerFr: `Manger en plein air.`, answerCn: `在户外吃饭。` },
          { id: 4, topicCn: "", answerFr: `Elle n’existe plus depuis un moment.`, answerCn: `它已经不存在一段时间了。` },
          { id: 5, topicCn: "", answerFr: `Pour parler de sa ville.`, answerCn: `为了谈论他的城市。` },
          { id: 6, topicCn: "", answerFr: `À quel moment il pourra poser des congés.`, answerCn: `什么时候可以请假。` },
          { id: 7, topicCn: "", answerFr: `Pour savoir quand il aura son carnet de chèques.`, answerCn: `了解何时能拿到支票簿。` },
          { id: 8, topicCn: "", answerFr: `Pour proposer un service.`, answerCn: `提供一项服务。` },
          { id: 9, topicCn: "", answerFr: `Il se rendra au théâtre.`, answerCn: `他会去剧院。` },

          { type: "section", titleCn: "T4", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Pour un renseignement.`, answerCn: `为了咨询信息。` },
          { id: 2, topicCn: "", answerFr: `Obtenir un logement.`, answerCn: `获得住房。` },
          { id: 3, topicCn: "", answerFr: `S’entretenir avec un enseignant.`, answerCn: `与老师交谈。` },
          { id: 4, topicCn: "", answerFr: `Leur collègue.`, answerCn: `他们的同事。` },
          { id: 5, topicCn: "", answerFr: `Il a trouvé qu’il y avait trop de visiteurs.`, answerCn: `他发现游客太多。` },
          { id: 6, topicCn: "", answerFr: `Passer le mois de juillet à Montpellier.`, answerCn: `七月在蒙彼利埃度过。` },
          { id: 7, topicCn: "", answerFr: `Elle aurait aimé faire du tourisme.`, answerCn: `她本想去旅游。` },
          { id: 8, topicCn: "", answerFr: `Parce que c’est inadapté à ses besoins.`, answerCn: `因为不符合她的需求。` },
          { id: 9, topicCn: "", answerFr: `Favoriser l’intégration des étrangers.`, answerCn: `促进外国人的融入。` },

          { type: "section", titleCn: "T5", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Monsieur Dupont a téléphoné et veut vous voir.`, answerCn: `Dupont先生打电话说想见你。` },
          { id: 2, topicCn: "", answerFr: `Monter à pied.`, answerCn: `步行上去。` },
          { id: 3, topicCn: "", answerFr: `Manger en plein air.`, answerCn: `在户外吃饭。` },
          { id: 4, topicCn: "", answerFr: `Un studio en ville.`, answerCn: `市中心的一间单间公寓。` },
          { id: 5, topicCn: "", answerFr: `Pour réparer des équipements informatiques.`, answerCn: `修理计算机设备。` },
          { id: 6, topicCn: "", answerFr: `Un manque d’activités de plein air.`, answerCn: `缺乏户外活动。` },
          { id: 7, topicCn: "", answerFr: `Prévenir d’un danger.`, answerCn: `提醒危险。` },
          { id: 8, topicCn: "", answerFr: `Son ami est définitivement employé dans la société où il travaille.`, answerCn: `他的朋友已正式受雇于公司。` },
          { id: 9, topicCn: "", answerFr: `De déjeuner ensemble.`, answerCn: `一起吃午饭。` },

          { type: "section", titleCn: "T6", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Au cinéma.`, answerCn: `在电影院。` },
          { id: 2, topicCn: "", answerFr: `De réserver rapidement.`, answerCn: `尽快预订。` },
          { id: 3, topicCn: "", answerFr: `Elle sait soigner les animaux sauvages.`, answerCn: `她会治疗野生动物。` },
          { id: 4, topicCn: "", answerFr: `En regardant jouer ses proches.`, answerCn: `看亲友比赛。` },
          { id: 5, topicCn: "", answerFr: `Pour réparer des équipements informatiques.`, answerCn: `修理电脑设备。` },
          { id: 6, topicCn: "", answerFr: `Il aura lieu plus tard dans le semestre.`, answerCn: `将在学期后期举行。` },
          { id: 7, topicCn: "", answerFr: `Vérifier si un courrier est bien arrivé.`, answerCn: `确认邮件是否已到达。` },
          { id: 8, topicCn: "", answerFr: `Elle a été victime d’un vol.`, answerCn: `她遭遇了盗窃。` },
          { id: 9, topicCn: "", answerFr: `Les départs sont nombreux.`, answerCn: `离开的人很多。` },

          { type: "section", titleCn: "T7", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle est située dans une rue bruyante.`, answerCn: `它位于一条嘈杂的街道。` },
          { id: 2, topicCn: "", answerFr: `Se mettre directement en contact avec l’université.`, answerCn: `直接与大学联系。` },
          { id: 3, topicCn: "", answerFr: `Créer l’occasion de se retrouver en famille.`, answerCn: `创造与家人团聚的机会。` },
          { id: 4, topicCn: "", answerFr: `Pour réparer des équipements informatiques.`, answerCn: `为了修理电脑设备。` },
          { id: 5, topicCn: "", answerFr: `L’accroissement de la population.`, answerCn: `人口增长。` },
          { id: 6, topicCn: "", answerFr: `À quel moment il pourra poser des congés.`, answerCn: `什么时候可以请假。` },
          { id: 7, topicCn: "", answerFr: `C’est une destination inadaptée pour les plus jeunes.`, answerCn: `这个目的地不适合年轻人。` },
          { id: 8, topicCn: "", answerFr: `Pour proposer un service.`, answerCn: `为了提供一项服务。` },
          { id: 9, topicCn: "", answerFr: `Il manque d’expérience.`, answerCn: `他缺乏经验。` },

          { type: "section", titleCn: "T8", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il sera en vacances.`, answerCn: `他将去度假。` },
          { id: 2, topicCn: "", answerFr: `Il baisse le volume.`, answerCn: `他把音量调低。` },
          { id: 3, topicCn: "", answerFr: `Monter à pied.`, answerCn: `步行上去。` },
          { id: 4, topicCn: "", answerFr: `La mission est sans intérêt.`, answerCn: `任务没有意义。` },
          { id: 5, topicCn: "", answerFr: `Elle n’a pas eu l’appel espéré.`, answerCn: `她没有接到期待的电话。` },
          { id: 6, topicCn: "", answerFr: `Il aura lieu plus tard dans le semestre.`, answerCn: `将在学期后期举行。` },
          { id: 7, topicCn: "", answerFr: `Devoir partir en voiture.`, answerCn: `必须开车离开。` },
          { id: 8, topicCn: "", answerFr: `Les difficultés en cas d’échange.`, answerCn: `交换时的困难。` },
          { id: 9, topicCn: "", answerFr: `Le recrutement se fonde sur l’expérience.`, answerCn: `招聘以经验为基础。` },

          { type: "section", titleCn: "T9", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle doit rappeler plus tard.`, answerCn: `她需要稍后再打电话。` },
          { id: 2, topicCn: "", answerFr: `S’entretenir avec un enseignant.`, answerCn: `与老师交谈。` },
          { id: 3, topicCn: "", answerFr: `Elle passe ses congés dans la région.`, answerCn: `她在本地区度假。` },
          { id: 4, topicCn: "", answerFr: `Un studio en ville.`, answerCn: `市中心的一间单间公寓。` },
          { id: 5, topicCn: "", answerFr: `Elle fait confiance à son guide.`, answerCn: `她信任她的导游。` },
          { id: 6, topicCn: "", answerFr: `Un propriétaire d’appartement.`, answerCn: `公寓房东。` },
          { id: 7, topicCn: "", answerFr: `Devoir partir en voiture.`, answerCn: `必须开车离开。` },
          { id: 8, topicCn: "", answerFr: `Parce que c’est inadapté à ses besoins.`, answerCn: `因为不适合她的需求。` },
          { id: 9, topicCn: "", answerFr: `Elles ont vu un film au cinéma.`, answerCn: `她们在电影院看了电影。` },

          { type: "section", titleCn: "T10", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `De vacances en famille.`, answerCn: `家庭度假。` },
          { id: 2, topicCn: "", answerFr: `L’annulation d’un cours.`, answerCn: `课程取消。` },
          { id: 3, topicCn: "", answerFr: `Travailler toute la journée.`, answerCn: `整天工作。` },
          { id: 4, topicCn: "", answerFr: `De partir ensemble à l’étranger.`, answerCn: `一起出国。` },
          { id: 5, topicCn: "", answerFr: `Monter d’un étage.`, answerCn: `上楼一层。` },
          { id: 6, topicCn: "", answerFr: `Elles vont rendre visite à une amie.`, answerCn: `她们将去拜访一位朋友。` },
          { id: 7, topicCn: "", answerFr: `Elle part en vacances en Grèce.`, answerCn: `她去希腊度假。` },
          { id: 8, topicCn: "", answerFr: `Revenir plus tard dans la journée.`, answerCn: `当天晚些时候再回来。` },
          { id: 9, topicCn: "", answerFr: `Envoyer une lettre.`, answerCn: `寄一封信。` },

          { type: "section", titleCn: "T11", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle a oublié un objet important.`, answerCn: `她忘了一个重要物品。` },
          { id: 2, topicCn: "", answerFr: `Dîner avec un ami.`, answerCn: `和朋友吃晚饭。` },
          { id: 3, topicCn: "", answerFr: `D’aller dans un bar.`, answerCn: `去酒吧。` },
          { id: 4, topicCn: "", answerFr: `Le contact avec les élèves.`, answerCn: `与学生接触。` },
          { id: 5, topicCn: "", answerFr: `Pour lui donner des informations.`, answerCn: `给他提供信息。` },
          { id: 6, topicCn: "", answerFr: `Elle apprécie beaucoup sa nouvelle ville.`, answerCn: `她非常喜欢她的新城市。` },
          { id: 7, topicCn: "", answerFr: `Elle aurait aimé faire du tourisme.`, answerCn: `她本想去旅游。` },
          { id: 8, topicCn: "", answerFr: `Elle accepte son invitation.`, answerCn: `她接受了邀请。` },
          { id: 9, topicCn: "", answerFr: `De jouer au basket-ball sans payer.`, answerCn: `免费打篮球。` },

          { type: "section", titleCn: "T12", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle doit quitter son logement.`, answerCn: `她必须搬离住所。` },
          { id: 2, topicCn: "", answerFr: `Parce que leur avion décolle bientôt.`, answerCn: `因为他们的飞机很快起飞。` },
          { id: 3, topicCn: "", answerFr: `Dans la poubelle.`, answerCn: `在垃圾桶里。` },
          { id: 4, topicCn: "", answerFr: `Le prix du séjour.`, answerCn: `旅行费用。` },
          { id: 5, topicCn: "", answerFr: `Pour lui rappeler une chose importante.`, answerCn: `提醒他一件重要的事情。` },
          { id: 6, topicCn: "", answerFr: `Pour lui proposer un entretien.`, answerCn: `向他提出面试。` },
          { id: 7, topicCn: "", answerFr: `Classer des documents.`, answerCn: `整理文件。` },
          { id: 8, topicCn: "", answerFr: `Elles modernisent leurs procédés de recrutement.`, answerCn: `他们使招聘方式现代化。` },
          { id: 9, topicCn: "", answerFr: `Des avantages du travail à distance.`, answerCn: `远程工作的优势。` },

          { type: "section", titleCn: "T13", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Prendre un train.`, answerCn: `乘火车。` },
          { id: 2, topicCn: "", answerFr: `Ils sont bénéfiques pour la santé.`, answerCn: `它们对健康有益。` },
          { id: 3, topicCn: "", answerFr: `De partir à l’étranger.`, answerCn: `去国外。` },
          { id: 4, topicCn: "", answerFr: `De se baigner dans les secteurs prévus.`, answerCn: `在指定区域游泳。` },
          { id: 5, topicCn: "", answerFr: `Le prix du séjour.`, answerCn: `旅行费用。` },
          { id: 6, topicCn: "", answerFr: `Une participation bénévole.`, answerCn: `志愿参与。` },
          { id: 7, topicCn: "", answerFr: `Il correspond à ses attentes.`, answerCn: `它符合他的期望。` },
          { id: 8, topicCn: "", answerFr: `Comment la santé est influencée par le calendrier.`, answerCn: `健康如何受日历影响。` },
          { id: 9, topicCn: "", answerFr: `Les départs sont nombreux.`, answerCn: `离开的人很多。` },

          { type: "section", titleCn: "T14", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `De cinéma.`, answerCn: `关于电影。` },
          { id: 2, topicCn: "", answerFr: `Il y a un service internet.`, answerCn: `有互联网服务。` },
          { id: 3, topicCn: "", answerFr: `Le prix du séjour.`, answerCn: `旅行费用。` },
          { id: 4, topicCn: "", answerFr: `Il a trouvé qu’il y avait trop de visiteurs.`, answerCn: `他发现游客太多。` },
          { id: 5, topicCn: "", answerFr: `Pour lui présenter un produit.`, answerCn: `向他介绍一个产品。` },
          { id: 6, topicCn: "", answerFr: `Son caractère.`, answerCn: `他的性格。` },
          { id: 7, topicCn: "", answerFr: `Sa qualification.`, answerCn: `他的资历。` },
          { id: 8, topicCn: "", answerFr: `Que son assistant l’avait perdu.`, answerCn: `他的助手把它弄丢了。` },
          { id: 9, topicCn: "", answerFr: `Elle va attendre un petit peu.`, answerCn: `她会稍等一会儿。` },

          { type: "section", titleCn: "T15", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Louer un appartement.`, answerCn: `租公寓。` },
          { id: 2, topicCn: "", answerFr: `D’un séjour linguistique.`, answerCn: `语言学习旅行。` },
          { id: 3, topicCn: "", answerFr: `D’aller dans un bar.`, answerCn: `去酒吧。` },
          { id: 4, topicCn: "", answerFr: `L’enfant est malade à cause des chats.`, answerCn: `孩子因为猫生病了。` },
          { id: 5, topicCn: "", answerFr: `Un studio en ville.`, answerCn: `城市里的单间公寓。` },
          { id: 6, topicCn: "", answerFr: `À quel moment il pourra poser des congés.`, answerCn: `什么时候可以请假。` },
          { id: 7, topicCn: "", answerFr: `Vérifier si un courrier est bien arrivé.`, answerCn: `确认邮件是否到达。` },
          { id: 8, topicCn: "", answerFr: `Elle est la destination d’une population migrante jeune.`, answerCn: `它是年轻移民人口的目的地。` },
          { id: 9, topicCn: "", answerFr: `Des avantages du travail à distance.`, answerCn: `远程工作的优势。` },

          { type: "section", titleCn: "T16", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Voir une exposition.`, answerCn: `看展览。` },
          { id: 2, topicCn: "", answerFr: `Dans la poubelle.`, answerCn: `在垃圾桶里。` },
          { id: 3, topicCn: "", answerFr: `Il y a un service internet.`, answerCn: `有互联网服务。` },
          { id: 4, topicCn: "", answerFr: `Le rôle des médiateurs en milieu scolaire.`, answerCn: `学校调解员的角色。` },
          { id: 5, topicCn: "", answerFr: `Elle fait confiance à son guide.`, answerCn: `她信任导游。` },
          { id: 6, topicCn: "", answerFr: `Parce qu’elle veut manger plus équilibré.`, answerCn: `因为她想吃得更健康。` },
          { id: 7, topicCn: "", answerFr: `Elles osent moins discuter leur contrat.`, answerCn: `她们不太敢讨论合同。` },
          { id: 8, topicCn: "", answerFr: `Elle propose des visites guidées.`, answerCn: `她提供导览服务。` },
          { id: 9, topicCn: "", answerFr: `Les activités en place.`, answerCn: `现有活动。` },

          { type: "section", titleCn: "T17", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Louer un appartement.`, answerCn: `租公寓。` },
          { id: 2, topicCn: "", answerFr: `Le chemin à suivre.`, answerCn: `要走的路线。` },
          { id: 3, topicCn: "", answerFr: `Le prix du séjour.`, answerCn: `旅行费用。` },
          { id: 4, topicCn: "", answerFr: `Parce qu’il manque d’information.`, answerCn: `因为信息不足。` },
          { id: 5, topicCn: "", answerFr: `Travailler toute la journée.`, answerCn: `整天工作。` },
          { id: 6, topicCn: "", answerFr: `Il aura lieu plus tard dans le semestre.`, answerCn: `将在学期后期举行。` },
          { id: 7, topicCn: "", answerFr: `Une participation bénévole.`, answerCn: `志愿参与。` },
          { id: 8, topicCn: "", answerFr: `De voir une compétition mondiale.`, answerCn: `观看世界级比赛。` },
          { id: 9, topicCn: "", answerFr: `L’affiche.`, answerCn: `海报。` },

          { type: "section", titleCn: "T18", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Le départ d’un vol.`, answerCn: `航班起飞。` },
          { id: 2, topicCn: "", answerFr: `Elle va voir un autre appartement.`, answerCn: `她去看另一套公寓。` },
          { id: 3, topicCn: "", answerFr: `Savoir si son véhicule est prêt.`, answerCn: `确认车辆是否准备好。` },
          { id: 4, topicCn: "", answerFr: `Parce qu’il manque d’information.`, answerCn: `因为信息不足。` },
          { id: 5, topicCn: "", answerFr: `Le contact avec les élèves.`, answerCn: `与学生接触。` },
          { id: 6, topicCn: "", answerFr: `Au restaurant.`, answerCn: `在餐厅。` },
          { id: 7, topicCn: "", answerFr: `Les lieux qui ont changé sous Napoléon.`, answerCn: `拿破仑时期改变的地点。` },
          { id: 8, topicCn: "", answerFr: `Il veut obtenir des renseignements.`, answerCn: `他想获取信息。` },
          { id: 9, topicCn: "", answerFr: `Elles ont vu un film au cinéma.`, answerCn: `她们在电影院看电影。` },

          { type: "section", titleCn: "T19", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle va travailler un mois.`, answerCn: `她将工作一个月。` },
          { id: 2, topicCn: "", answerFr: `Un trafic trop dense.`, answerCn: `交通过于拥堵。` },
          { id: 3, topicCn: "", answerFr: `Dîner avec un ami.`, answerCn: `和朋友吃晚饭。` },
          { id: 4, topicCn: "", answerFr: `Les conditions de visite.`, answerCn: `参观条件。` },
          { id: 5, topicCn: "", answerFr: `Se renseigner au guichet.`, answerCn: `到柜台咨询。` },
          { id: 6, topicCn: "", answerFr: `Pour parler de sa ville.`, answerCn: `为了谈论他的城市。` },
          { id: 7, topicCn: "", answerFr: `À quel moment il pourra poser des congés.`, answerCn: `什么时候他可以请假。` },
          { id: 8, topicCn: "", answerFr: `De mettre en contact des personnes pour partager du matériel.`, answerCn: `让人们互相联系以共享设备。` },
          { id: 9, topicCn: "", answerFr: `Les conditions de recrutement sont plus difficiles aujourd’hui.`, answerCn: `如今招聘条件更加困难。` },

          { type: "section", titleCn: "T20", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle a oublié un objet important.`, answerCn: `她忘记了一个重要物品。` },
          { id: 2, topicCn: "", answerFr: `De partir à l’étranger.`, answerCn: `去国外。` },
          { id: 3, topicCn: "", answerFr: `D’aller à l’université à pied.`, answerCn: `步行去大学。` },
          { id: 4, topicCn: "", answerFr: `Il est vraiment beau.`, answerCn: `他真的很帅。` },
          { id: 5, topicCn: "", answerFr: `Travailler toute la journée.`, answerCn: `整天工作。` },
          { id: 6, topicCn: "", answerFr: `Les véhicules qui circulent près de chez lui.`, answerCn: `他家附近的车辆。` },
          { id: 7, topicCn: "", answerFr: `Pour lui dire qu’elle est retenue au bureau.`, answerCn: `告诉他她被工作耽搁了。` },
          { id: 8, topicCn: "", answerFr: `De jouer au basket-ball sans payer.`, answerCn: `免费打篮球。` },
          { id: 9, topicCn: "", answerFr: `Récupérer son argent.`, answerCn: `取回他的钱。` },

          { type: "section", titleCn: "T21", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle a oublié un objet important.`, answerCn: `她忘记了一个重要物品。` },
          { id: 2, topicCn: "", answerFr: `De partir à l’étranger.`, answerCn: `去国外。` },
          { id: 3, topicCn: "", answerFr: `Le prix du séjour.`, answerCn: `旅行费用。` },
          { id: 4, topicCn: "", answerFr: `L’utilisation des médias.`, answerCn: `媒体的使用。` },
          { id: 5, topicCn: "", answerFr: `Le contact avec les élèves.`, answerCn: `与学生接触。` },
          { id: 6, topicCn: "", answerFr: `Pour lui donner des informations.`, answerCn: `给他提供信息。` },
          { id: 7, topicCn: "", answerFr: `L’histoire est compliquée.`, answerCn: `故事很复杂。` },
          { id: 8, topicCn: "", answerFr: `Pour proposer un service.`, answerCn: `提供服务。` },
          { id: 9, topicCn: "", answerFr: `Le recrutement se fonde sur l’expérience.`, answerCn: `招聘基于经验。` },

          { type: "section", titleCn: "T22", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il est malade avec les crevettes.`, answerCn: `他对虾过敏。` },
          { id: 2, topicCn: "", answerFr: `Savoir si son véhicule est prêt.`, answerCn: `确认他的车辆是否准备好了。` },
          { id: 3, topicCn: "", answerFr: `Du dernier film qu’elles ont vu.`, answerCn: `她们最近看的电影。` },
          { id: 4, topicCn: "", answerFr: `Le contact avec les élèves.`, answerCn: `与学生接触。` },
          { id: 5, topicCn: "", answerFr: `Les véhicules qui circulent près de chez lui.`, answerCn: `他家附近行驶的车辆。` },
          { id: 6, topicCn: "", answerFr: `L’histoire est compliquée.`, answerCn: `故事很复杂。` },
          { id: 7, topicCn: "", answerFr: `Le justificatif d’achat.`, answerCn: `购买凭证。` },
          { id: 8, topicCn: "", answerFr: `Un reportage sur les lieux d’un tremblement de terre.`, answerCn: `关于地震现场的报道。` },
          { id: 9, topicCn: "", answerFr: `De jouer au basket-ball sans payer.`, answerCn: `免费打篮球。` },

          { type: "section", titleCn: "T23", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Se connecter sur le site Internet.`, answerCn: `登录网站。` },
          { id: 2, topicCn: "", answerFr: `Les relations avec les enseignants.`, answerCn: `与老师的关系。` },
          { id: 3, topicCn: "", answerFr: `Du dernier film qu’elles ont vu.`, answerCn: `她们最近看的电影。` },
          { id: 4, topicCn: "", answerFr: `Appuyer sur le bouton indiqué.`, answerCn: `按下指定按钮。` },
          { id: 5, topicCn: "", answerFr: `Il a besoin de travaux.`, answerCn: `它需要维修。` },
          { id: 6, topicCn: "", answerFr: `Un propriétaire d’appartement.`, answerCn: `一位公寓房东。` },
          { id: 7, topicCn: "", answerFr: `Elle accepte son invitation.`, answerCn: `她接受了邀请。` },
          { id: 8, topicCn: "", answerFr: `Les difficultés en cas d’échange.`, answerCn: `交换时的困难。` },
          { id: 9, topicCn: "", answerFr: `Il travaille pour plusieurs entreprises.`, answerCn: `他为多家公司工作。` },

          { type: "section", titleCn: "T24", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle est située dans une rue bruyante.`, answerCn: `它位于一条嘈杂的街道。` },
          { id: 2, topicCn: "", answerFr: `Se mettre directement en contact avec l’université.`, answerCn: `直接联系大学。` },
          { id: 3, topicCn: "", answerFr: `D’un séjour linguistique.`, answerCn: `一次语言学习旅行。` },
          { id: 4, topicCn: "", answerFr: `Pour réparer des équipements informatiques.`, answerCn: `修理电脑设备。` },
          { id: 5, topicCn: "", answerFr: `Le rôle des médiateurs en milieu scolaire.`, answerCn: `学校调解员的角色。` },
          { id: 6, topicCn: "", answerFr: `Les véhicules qui circulent près de chez lui.`, answerCn: `他家附近的车辆。` },
          { id: 7, topicCn: "", answerFr: `Les lieux qui ont changé sous Napoléon.`, answerCn: `拿破仑时期改变的地点。` },
          { id: 8, topicCn: "", answerFr: `Un reportage sur les lieux d’un tremblement de terre.`, answerCn: `关于地震现场的报道。` },
          { id: 9, topicCn: "", answerFr: `Les départs sont nombreux.`, answerCn: `离开的人很多。` },

          { type: "section", titleCn: "T25", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Les saisons.`, answerCn: `季节。` },
          { id: 2, topicCn: "", answerFr: `Leur collègue.`, answerCn: `他们的同事。` },
          { id: 3, topicCn: "", answerFr: `Le rôle des médiateurs en milieu scolaire.`, answerCn: `学校调解员的作用。` },
          { id: 4, topicCn: "", answerFr: `Remettre un vêtement au vestiaire.`, answerCn: `把衣服放到衣帽间。` },
          { id: 5, topicCn: "", answerFr: `Pour parler de sa ville.`, answerCn: `为了谈论他的城市。` },
          { id: 6, topicCn: "", answerFr: `L’accroissement de la population.`, answerCn: `人口增长。` },
          { id: 7, topicCn: "", answerFr: `Pour annoncer un retard.`, answerCn: `通知迟到。` },
          { id: 8, topicCn: "", answerFr: `Les difficultés en cas d’échange.`, answerCn: `交换时的困难。` },
          { id: 9, topicCn: "", answerFr: `De déjeuner ensemble.`, answerCn: `一起吃午饭。` },

          { type: "section", titleCn: "T26", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Voir une exposition.`, answerCn: `看展览。` },
          { id: 2, topicCn: "", answerFr: `Les cours ont lieu en journée.`, answerCn: `课程在白天进行。` },
          { id: 3, topicCn: "", answerFr: `Leur collègue.`, answerCn: `他们的同事。` },
          { id: 4, topicCn: "", answerFr: `Un vêtement de plage.`, answerCn: `一件海滩服装。` },
          { id: 5, topicCn: "", answerFr: `L’utilisation des médias.`, answerCn: `媒体的使用。` },
          { id: 6, topicCn: "", answerFr: `Obtenir une aide financière.`, answerCn: `获得经济援助。` },
          { id: 7, topicCn: "", answerFr: `Pour savoir quand il aura son carnet de chèques.`, answerCn: `了解何时能拿到支票簿。` },
          { id: 8, topicCn: "", answerFr: `De jouer au basket-ball sans payer.`, answerCn: `免费打篮球。` },
          { id: 9, topicCn: "", answerFr: `L’inadéquation entre l’université et le monde du travail.`, answerCn: `大学与就业市场之间的不匹配。` },

          { type: "section", titleCn: "T27", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Pour faire un contrôle médical.`, answerCn: `进行体检。` },
          { id: 2, topicCn: "", answerFr: `Dans la poubelle.`, answerCn: `在垃圾桶里。` },
          { id: 3, topicCn: "", answerFr: `D’aller à l’université à pied.`, answerCn: `步行去大学。` },
          { id: 4, topicCn: "", answerFr: `Il est vraiment beau.`, answerCn: `他真的很帅。` },
          { id: 5, topicCn: "", answerFr: `Se renseigner au guichet.`, answerCn: `到柜台咨询。` },
          { id: 6, topicCn: "", answerFr: `Une élection.`, answerCn: `一次选举。` },
          { id: 7, topicCn: "", answerFr: `Prévenir d’un danger.`, answerCn: `提醒危险。` },
          { id: 8, topicCn: "", answerFr: `De voir une compétition mondiale.`, answerCn: `观看世界级比赛。` },
          { id: 9, topicCn: "", answerFr: `Elles ont vu un film au cinéma.`, answerCn: `她们在电影院看电影。` },

          { type: "section", titleCn: "T28", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle a oublié un objet important.`, answerCn: `她忘记了一个重要物品。` },
          { id: 2, topicCn: "", answerFr: `D’un nouveau produit.`, answerCn: `一种新产品。` },
          { id: 3, topicCn: "", answerFr: `Il y a un service internet.`, answerCn: `有互联网服务。` },
          { id: 4, topicCn: "", answerFr: `Elle a testé un nouveau bar.`, answerCn: `她尝试了一家新酒吧。` },
          { id: 5, topicCn: "", answerFr: `Pour lui donner des informations.`, answerCn: `给他提供信息。` },
          { id: 6, topicCn: "", answerFr: `Pour annoncer un retard.`, answerCn: `通知迟到。` },
          { id: 7, topicCn: "", answerFr: `Pour avoir un logement plus grand et peu cher.`, answerCn: `为了得到更大更便宜的住房。` },
          { id: 8, topicCn: "", answerFr: `Elle a été victime d’un vol.`, answerCn: `她遭遇了盗窃。` },
          { id: 9, topicCn: "", answerFr: `De déjeuner ensemble.`, answerCn: `一起吃午饭。` },

          { type: "section", titleCn: "T29", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Participer à une formation.`, answerCn: `参加培训。` },
          { id: 2, topicCn: "", answerFr: `D’un séjour linguistique.`, answerCn: `语言学习旅行。` },
          { id: 3, topicCn: "", answerFr: `D’aller à l’université à pied.`, answerCn: `步行去大学。` },
          { id: 4, topicCn: "", answerFr: `Pour annuler leurs vacances.`, answerCn: `取消他们的假期。` },
          { id: 5, topicCn: "", answerFr: `Il a trouvé qu’il y avait trop de visiteurs.`, answerCn: `他发现游客太多。` },
          { id: 6, topicCn: "", answerFr: `Un repas entre collègues.`, answerCn: `同事聚餐。` },
          { id: 7, topicCn: "", answerFr: `Le service après-vente est payant.`, answerCn: `售后服务是收费的。` },
          { id: 8, topicCn: "", answerFr: `Il veut obtenir des renseignements.`, answerCn: `他想获取信息。` },
          { id: 9, topicCn: "", answerFr: `Elle va attendre un petit peu.`, answerCn: `她会稍等一会儿。` },

          { type: "section", titleCn: "T30", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Les saisons.`, answerCn: `季节。` },
          { id: 2, topicCn: "", answerFr: `D’un séjour linguistique.`, answerCn: `语言学习旅行。` },
          { id: 3, topicCn: "", answerFr: `Il a été très agréablement surpris.`, answerCn: `他感到非常惊喜。` },
          { id: 4, topicCn: "", answerFr: `De partir ensemble à l’étranger.`, answerCn: `一起出国。` },
          { id: 5, topicCn: "", answerFr: `Pour parler de sa ville.`, answerCn: `谈论他的城市。` },
          { id: 6, topicCn: "", answerFr: `L’accroissement de la population.`, answerCn: `人口增长。` },
          { id: 7, topicCn: "", answerFr: `Pour avoir un logement plus grand et peu cher.`, answerCn: `获得更大更便宜的住房。` },
          { id: 8, topicCn: "", answerFr: `Pratiquer régulièrement un sport.`, answerCn: `定期运动。` },
          { id: 9, topicCn: "", answerFr: `Il manque d’expérience.`, answerCn: `他缺乏经验。` },

          { type: "section", titleCn: "T31", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un roman.`, answerCn: `一本小说。` },
          { id: 2, topicCn: "", answerFr: `Il a été très agréablement surpris.`, answerCn: `他感到非常惊喜。` },
          { id: 3, topicCn: "", answerFr: `Un vêtement de plage.`, answerCn: `一件海滩服装。` },
          { id: 4, topicCn: "", answerFr: `Prendre contact avec sa banque.`, answerCn: `联系他的银行。` },
          { id: 5, topicCn: "", answerFr: `Elle n’existe plus depuis un moment.`, answerCn: `它已经不存在一段时间。` },
          { id: 6, topicCn: "", answerFr: `Il connaissait peu le pays.`, answerCn: `他对这个国家不太了解。` },
          { id: 7, topicCn: "", answerFr: `D’aller au travail ensemble.`, answerCn: `一起去上班。` },
          { id: 8, topicCn: "", answerFr: `Il a payé ses billets trop cher.`, answerCn: `他的票买得太贵。` },
          { id: 9, topicCn: "", answerFr: `C’est une interprète sincère.`, answerCn: `她是一位真诚的翻译。` },

          { type: "section", titleCn: "T32", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un médecin.`, answerCn: `一位医生。` },
          { id: 2, topicCn: "", answerFr: `De leurs prochaines vacances.`, answerCn: `他们接下来的假期。` },
          { id: 3, topicCn: "", answerFr: `Les conditions de visite.`, answerCn: `参观条件。` },
          { id: 4, topicCn: "", answerFr: `Prendre contact avec sa banque.`, answerCn: `联系他的银行。` },
          { id: 5, topicCn: "", answerFr: `Elle n’a pas eu l’appel espéré.`, answerCn: `她没有接到期待的电话。` },
          { id: 6, topicCn: "", answerFr: `Elle fait confiance à son guide.`, answerCn: `她信任导游。` },
          { id: 7, topicCn: "", answerFr: `Il correspond à ses attentes.`, answerCn: `它符合他的期望。` },
          { id: 8, topicCn: "", answerFr: `De mettre en contact des personnes pour partager du matériel.`, answerCn: `联系他人共享设备。` },
          { id: 9, topicCn: "", answerFr: `D’informer de son retard.`, answerCn: `通知迟到。` },

          { type: "section", titleCn: "T33", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `De vacances en famille.`, answerCn: `家庭度假。` },
          { id: 2, topicCn: "", answerFr: `Obtenir un logement.`, answerCn: `获得住房。` },
          { id: 3, topicCn: "", answerFr: `Dîner avec un ami.`, answerCn: `与朋友吃晚饭。` },
          { id: 4, topicCn: "", answerFr: `La mission est sans intérêt.`, answerCn: `任务没有意义。` },
          { id: 5, topicCn: "", answerFr: `De partir ensemble à l’étranger.`, answerCn: `一起出国。` },
          { id: 6, topicCn: "", answerFr: `L’accroissement de la population.`, answerCn: `人口增长。` },
          { id: 7, topicCn: "", answerFr: `Elle aurait aimé faire du tourisme.`, answerCn: `她本想去旅游。` },
          { id: 8, topicCn: "", answerFr: `Comment la santé est influencée par le calendrier.`, answerCn: `健康如何受日历影响。` },
          { id: 9, topicCn: "", answerFr: `De jouer au basket-ball sans payer.`, answerCn: `免费打篮球。` },

          { type: "section", titleCn: "T34", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle a oublié un objet important.`, answerCn: `她忘记了一个重要物品。` },
          { id: 2, topicCn: "", answerFr: `Il a été très agréablement surpris.`, answerCn: `他非常惊喜。` },
          { id: 3, topicCn: "", answerFr: `Travailler toute la journée.`, answerCn: `整天工作。` },
          { id: 4, topicCn: "", answerFr: `La mission est sans intérêt.`, answerCn: `任务没有意义。` },
          { id: 5, topicCn: "", answerFr: `Pour lui présenter un produit.`, answerCn: `向他介绍产品。` },
          { id: 6, topicCn: "", answerFr: `L’histoire est compliquée.`, answerCn: `故事很复杂。` },
          { id: 7, topicCn: "", answerFr: `Le justificatif d’achat.`, answerCn: `购买凭证。` },
          { id: 8, topicCn: "", answerFr: `Pour proposer un service.`, answerCn: `提供服务。` },
          { id: 9, topicCn: "", answerFr: `Il manque d’expérience.`, answerCn: `他缺乏经验。` },

          { type: "section", titleCn: "T35", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Utiliser internet.`, answerCn: `使用互联网。` },
          { id: 2, topicCn: "", answerFr: `Utiliser la salle informatique.`, answerCn: `使用电脑室。` },
          { id: 3, topicCn: "", answerFr: `Pour lui rappeler une chose importante.`, answerCn: `提醒他一件重要事情。` },
          { id: 4, topicCn: "", answerFr: `Avoir le Baccalauréat.`, answerCn: `获得高中毕业证。` },
          { id: 5, topicCn: "", answerFr: `Au restaurant.`, answerCn: `在餐厅。` },
          { id: 6, topicCn: "", answerFr: `Pour se plaindre d’une commande non livrée.`, answerCn: `投诉未送达的订单。` },
          { id: 7, topicCn: "", answerFr: `Comment la santé est influencée par le calendrier.`, answerCn: `健康如何受日历影响。` },
          { id: 8, topicCn: "", answerFr: `D’informer de son retard.`, answerCn: `通知迟到。` },
          { id: 9, topicCn: "", answerFr: `Les conditions de recrutement sont plus difficiles aujourd’hui.`, answerCn: `如今招聘条件更困难。` },

          { type: "section", titleCn: "T36", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Son projet artistique.`, answerCn: `他的艺术项目。` },
          { id: 2, topicCn: "", answerFr: `Il doit parler avec son responsable.`, answerCn: `他必须和负责人谈话。` },
          { id: 3, topicCn: "", answerFr: `Le rôle des médiateurs en milieu scolaire.`, answerCn: `学校调解员的角色。` },
          { id: 4, topicCn: "", answerFr: `Remettre un vêtement au vestiaire.`, answerCn: `把衣服放到衣帽间。` },
          { id: 5, topicCn: "", answerFr: `D’essayer un vêtement près du corps.`, answerCn: `试穿贴身衣服。` },
          { id: 6, topicCn: "", answerFr: `L’accroissement de la population.`, answerCn: `人口增长。` },
          { id: 7, topicCn: "", answerFr: `Il espère que sa femme pourra venir au Canada.`, answerCn: `他希望妻子能来加拿大。` },
          { id: 8, topicCn: "", answerFr: `Il veut obtenir des renseignements.`, answerCn: `他想获取信息。` },
          { id: 9, topicCn: "", answerFr: `D’informer de son retard.`, answerCn: `通知迟到。` },

          { type: "section", titleCn: "T37", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Manger équilibré.`, answerCn: `饮食均衡。` },
          { id: 2, topicCn: "", answerFr: `D’un nouveau produit.`, answerCn: `一种新产品。` },
          { id: 3, topicCn: "", answerFr: `Ils doivent changer de moyen de transport.`, answerCn: `他们必须换一种交通方式。` },
          { id: 4, topicCn: "", answerFr: `Construire des objets à partir de skis usés.`, answerCn: `用旧滑雪板制作物品。` },
          { id: 5, topicCn: "", answerFr: `Travailler toute la journée.`, answerCn: `整天工作。` },
          { id: 6, topicCn: "", answerFr: `Il sait bien faire la cuisine.`, answerCn: `他很会做饭。` },
          { id: 7, topicCn: "", answerFr: `Devoir partir en voiture.`, answerCn: `必须开车离开。` },
          { id: 8, topicCn: "", answerFr: `Profiter d’une atmosphère familiale.`, answerCn: `享受家庭氛围。` },
          { id: 9, topicCn: "", answerFr: `Le voyage est trop long.`, answerCn: `旅途太长。` },

          { type: "section", titleCn: "T38", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle a dû marcher jusqu’au travail.`, answerCn: `她不得不走路去上班。` },
          { id: 2, topicCn: "", answerFr: `Dans la poubelle.`, answerCn: `在垃圾桶里。` },
          { id: 3, topicCn: "", answerFr: `Parce qu’il en reste encore chez elles.`, answerCn: `因为她们那里还有。` },
          { id: 4, topicCn: "", answerFr: `Elle n’existe plus depuis un moment.`, answerCn: `它已经不存在一段时间。` },
          { id: 5, topicCn: "", answerFr: `Un repas entre collègues.`, answerCn: `同事聚餐。` },
          { id: 6, topicCn: "", answerFr: `Il sait bien faire la cuisine.`, answerCn: `他很会做饭。` },
          { id: 7, topicCn: "", answerFr: `Il correspond à ses attentes.`, answerCn: `它符合他的期望。` },
          { id: 8, topicCn: "", answerFr: `Elle est la destination d’une population migrante jeune.`, answerCn: `它是年轻移民人口的目的地。` },
          { id: 9, topicCn: "", answerFr: `Chez un libraire.`, answerCn: `在书店。` },

          { type: "section", titleCn: "T39", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Participer à une formation.`, answerCn: `参加培训。` },
          { id: 2, topicCn: "", answerFr: `De partir à l’étranger.`, answerCn: `去国外。` },
          { id: 3, topicCn: "", answerFr: `Étiqueter ses bagages.`, answerCn: `给行李贴标签。` },
          { id: 4, topicCn: "", answerFr: `De se motiver pour rédiger des textes.`, answerCn: `激励自己写文章。` },
          { id: 5, topicCn: "", answerFr: `Il sait bien faire la cuisine.`, answerCn: `他很会做饭。` },
          { id: 6, topicCn: "", answerFr: `Un manque d’activités de plein air.`, answerCn: `缺乏户外活动。` },
          { id: 7, topicCn: "", answerFr: `Elles osent moins discuter leur contrat.`, answerCn: `她们不太敢讨论合同。` },
          { id: 8, topicCn: "", answerFr: `Elle est la destination d’une population migrante jeune.`, answerCn: `它是年轻移民人口的目的地。` },
          { id: 9, topicCn: "", answerFr: `D’informer de son retard.`, answerCn: `通知迟到。` },

          { type: "section", titleCn: "T40", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Les saisons.`, answerCn: `季节。` },
          { id: 2, topicCn: "", answerFr: `Leur collègue.`, answerCn: `他们的同事。` },
          { id: 3, topicCn: "", answerFr: `Le rôle des médiateurs en milieu scolaire.`, answerCn: `学校调解员的角色。` },
          { id: 4, topicCn: "", answerFr: `Remettre un vêtement au vestiaire.`, answerCn: `把衣服放到衣帽间。` },
          { id: 5, topicCn: "", answerFr: `Pour lui rappeler une chose importante.`, answerCn: `提醒他一件重要事情。` },
          { id: 6, topicCn: "", answerFr: `Pour lui proposer un entretien.`, answerCn: `向他提出面试。` },
          { id: 7, topicCn: "", answerFr: `Vérifier si un courrier est bien arrivé.`, answerCn: `确认邮件是否到达。` },
          { id: 8, topicCn: "", answerFr: `Elle est la destination d’une population migrante jeune.`, answerCn: `它是年轻移民人口的目的地。` },
          { id: 9, topicCn: "", answerFr: `Elle va attendre un petit peu.`, answerCn: `她会稍等一会儿。` },

          { type: "section", titleCn: "新题", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle a réalisé un projet artistique.`, answerCn: `她完成了一个艺术项目。` },
          { id: 2, topicCn: "", answerFr: `Être ouvert aux autres.`, answerCn: `对他人保持开放、愿意接纳他人。` },
          { id: 3, topicCn: "", answerFr: `Parce qu'il en reste encore chez elles.`, answerCn: `因为她们那里还剩下一些。` },
        ];
"""

# ---- Config ----
TACHE = 1             # change to 2/3 if you want
KIND = "a"               # "a" for answers; if you insist, change to "q"
OUT_CSV = Path("assets/tcfcaCO/t1.csv")
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
