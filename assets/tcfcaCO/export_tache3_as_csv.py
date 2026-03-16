#!/usr/bin/env python3
import csv
import re
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
[

          // ── T01 ──
          { type: "section", titleCn: "T01", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Le système génétique est affecté`, answerCn: `遗传系统受到了影响` },
          { id: 2, topicCn: "", answerFr: `L'absence totale des signes visuels du langage`, answerCn: `完全缺乏语言的视觉符号` },
          { id: 3, topicCn: "", answerFr: `Si on modifie la façon dont on les perçoit`, answerCn: `如果改变我们感知它们的方式` },
          { id: 4, topicCn: "", answerFr: `Le déroulement des événements`, answerCn: `事件的经过` },
          { id: 5, topicCn: "", answerFr: `Ils présentent un partage sexiste des tâches dans le couple`, answerCn: `它们呈现出伴侣间带有性别偏见的分工` },
          { id: 6, topicCn: "", answerFr: `Il existerait un ordre universel de la pensée, indépendant de l'ordre linguistique`, answerCn: `存在一种独立于语言秩序的普遍思维秩序` },

          // ── T02 ──
          { type: "section", titleCn: "T02", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La méfiance des propriétaires`, answerCn: `业主的不信任` },
          { id: 2, topicCn: "", answerFr: `L'accès réglementé à un emplacement protégé`, answerCn: `对受保护地点的受限访问` },
          { id: 3, topicCn: "", answerFr: `L'absence de prise de décisions effectives`, answerCn: `缺乏有效的决策` },
          { id: 4, topicCn: "", answerFr: `Elle permet le dépassement des normes édictées`, answerCn: `它使超越既定规范成为可能` },
          { id: 5, topicCn: "", answerFr: `L'extension d'un système de climatisation à tout un quartier`, answerCn: `将空调系统扩展至整个街区` },
          { id: 6, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels`, answerCn: `他对传统媒体的价值持怀疑态度` },

          // ── T03 ──
          { type: "section", titleCn: "T03", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il donne un conseil`, answerCn: `他给出一条建议` },
          { id: 2, topicCn: "", answerFr: `Les réticences émises par la clientèle`, answerCn: `客户所表达的顾虑` },
          { id: 3, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共情` },
          { id: 4, topicCn: "", answerFr: `Les intérêts en jeu sont difficilement compatibles`, answerCn: `相关利益难以协调` },
          { id: 5, topicCn: "", answerFr: `Donner une dimension nouvelle aux lieux mis en scène`, answerCn: `赋予场景中的地点新的维度` },
          { id: 6, topicCn: "", answerFr: `À minimiser les aléas`, answerCn: `将不确定性降到最低` },

          // ── T04 ──
          { type: "section", titleCn: "T04", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La méfiance des propriétaires`, answerCn: `业主的不信任` },
          { id: 2, topicCn: "", answerFr: `Permettre aux jeunes de découvrir un sport difficile`, answerCn: `让年轻人了解一项有难度的运动` },
          { id: 3, topicCn: "", answerFr: `Il se réfugiait dans le dessin pour échapper à ses camarades`, answerCn: `他躲进绘画世界以逃避同伴` },
          { id: 4, topicCn: "", answerFr: `Diffuser l'art dans des endroits inattendus`, answerCn: `在意想不到的地方传播艺术` },
          { id: 5, topicCn: "", answerFr: `Le déroulement des événements`, answerCn: `事件的经过` },
          { id: 6, topicCn: "", answerFr: `En abandonnant les codes traditionnels du roman`, answerCn: `摒弃小说的传统规范` },

          // ── T05 ──
          { type: "section", titleCn: "T05", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Permet de découvrir les saveurs antillaises`, answerCn: `让人发现安的列斯群岛的风味` },
          { id: 2, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多地诉诸理性` },
          { id: 3, topicCn: "", answerFr: `Pour sortir de la crise que son économie subissait`, answerCn: `为了摆脱其经济所遭受的危机` },
          { id: 4, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在应当得到官方认可` },
          { id: 5, topicCn: "", answerFr: `Une analyse du contexte socio-éducatif actuel`, answerCn: `对当前社会教育背景的分析` },
          { id: 6, topicCn: "", answerFr: `La singularité de ses portraits`, answerCn: `其人物肖像的独特性` },

          // ── T06 ──
          { type: "section", titleCn: "T06", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L'utilisation abusive de flashbacks`, answerCn: `过度使用闪回手法` },
          { id: 2, topicCn: "", answerFr: `La 200e édition d'une émission`, answerCn: `某节目的第200期` },
          { id: 3, topicCn: "", answerFr: `Il du mal à se déplacer dans la foule`, answerCn: `他难以在人群中穿行` },
          { id: 4, topicCn: "", answerFr: `Exploiter les compétences acquises`, answerCn: `充分发挥所学技能` },
          { id: 5, topicCn: "", answerFr: `Ils présentent un partage sexiste des tâches dans le couple`, answerCn: `它们呈现出伴侣间带有性别偏见的分工` },
          { id: 6, topicCn: "", answerFr: `Il se sentait trop vieux pour les tournées`, answerCn: `他觉得自己年纪太大，不适合巡演了` },

          // ── T07 ──
          { type: "section", titleCn: "T07", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Un couple qui ne s'aime plus`, answerCn: `一对不再相爱的夫妻` },
          { id: 2, topicCn: "", answerFr: `En s'enrichissant de tous types d'apports`, answerCn: `通过吸收各种类型的贡献而得到丰富` },
          { id: 3, topicCn: "", answerFr: `Il est indispensable de savoir s'en servir correctement`, answerCn: `必须懂得正确使用它` },
          { id: 4, topicCn: "", answerFr: `Elle répond à certaines règles compréhensibles`, answerCn: `它遵循一些可理解的规则` },
          { id: 5, topicCn: "", answerFr: `Le déroulement des événements`, answerCn: `事件的经过` },
          { id: 6, topicCn: "", answerFr: `De satisfaire avant tout les adultes`, answerCn: `首先要满足成年人的需求` },

          // ── T08 ──
          { type: "section", titleCn: "T08", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle doit se fonder sur l'estime mutuelle`, answerCn: `它必须建立在相互尊重的基础上` },
          { id: 2, topicCn: "", answerFr: `L'absence totale des signes visuels du langage`, answerCn: `完全缺乏语言的视觉符号` },
          { id: 3, topicCn: "", answerFr: `Pour sortir de la crise que son économie subissait`, answerCn: `为了摆脱其经济所遭受的危机` },
          { id: 4, topicCn: "", answerFr: `La société actuelle accepte mal qu'un enfant soit élevé uniquement par son père`, answerCn: `当今社会难以接受孩子只由父亲抚养的情况` },
          { id: 5, topicCn: "", answerFr: `Il existerait un ordre universel de la pensée indépendamment de l'ordre linguistique`, answerCn: `存在一种独立于语言秩序的普遍思维秩序` },
          { id: 6, topicCn: "", answerFr: `De satisfaire avant tout les adultes`, answerCn: `首先要满足成年人的需求` },

          // ── T09 ──
          { type: "section", titleCn: "T09", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Profiter d'un encadrement spécifique`, answerCn: `利用专项指导框架` },
          { id: 2, topicCn: "", answerFr: `Son charisme incroyable`, answerCn: `他令人难以置信的个人魅力` },
          { id: 3, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与对数字世界的探索` },
          { id: 4, topicCn: "", answerFr: `Diffuser l'art dans des endroits inattendus`, answerCn: `在意想不到的地方传播艺术` },
          { id: 5, topicCn: "", answerFr: `Dans un parc naturel`, answerCn: `在一处自然公园中` },
          { id: 6, topicCn: "", answerFr: `Il insiste sur le point de vue matériel`, answerCn: `他强调物质层面的观点` },

          // ── T10 ──
          { type: "section", titleCn: "T10", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Demande à une cliente de payer l'intégralité de sa commande`, answerCn: `要求顾客全额支付订单` },
          { id: 2, topicCn: "", answerFr: `Des passionnés de randonnée`, answerCn: `徒步爱好者` },
          { id: 3, topicCn: "", answerFr: `Il était déjà, en son temps, un artiste reconnu par ses pairs`, answerCn: `他在当时已是一位受同行认可的艺术家` },
          { id: 4, topicCn: "", answerFr: `C'est un marqueur social`, answerCn: `这是一种社会标志` },
          { id: 5, topicCn: "", answerFr: `La société actuelle accepte mal qu'un enfant élevé uniquement par son père`, answerCn: `当今社会难以接受孩子只由父亲抚养的情况` },
          { id: 6, topicCn: "", answerFr: `Le raisonnement du penseur représente une entrave à la création`, answerCn: `这位思想家的推理方式对创作构成了阻碍` },

          // ── T11 ──
          { type: "section", titleCn: "T11", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La rivalité entre les différents médias`, answerCn: `不同媒体之间的竞争` },
          { id: 2, topicCn: "", answerFr: `Les réticences émises par la clientèle`, answerCn: `客户所表达的顾虑` },
          { id: 3, topicCn: "", answerFr: `Les financements publics contribuent à leur expansion`, answerCn: `公共资助促进了它们的扩张` },
          { id: 4, topicCn: "", answerFr: `Elle permet le dépassement des normes édictées`, answerCn: `它使超越既定规范成为可能` },
          { id: 5, topicCn: "", answerFr: `La mise en place de la démocratie résulte d'un long processus`, answerCn: `民主制度的建立是一个漫长过程的结果` },
          { id: 6, topicCn: "", answerFr: `Il insiste sur le point de vue matériel`, answerCn: `他强调物质层面的观点` },

          // ── T12 ──
          { type: "section", titleCn: "T12", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科上为自己设定了较高的目标` },
          { id: 2, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不受重视的艺术形式` },
          { id: 3, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众的对话` },
          { id: 4, topicCn: "", answerFr: `Elle permet le dépassement des normes édictées`, answerCn: `它使超越既定规范成为可能` },
          { id: 5, topicCn: "", answerFr: `L'extension d'un système de climatisation à tout un quartier`, answerCn: `将空调系统扩展至整个街区` },
          { id: 6, topicCn: "", answerFr: `Il s'indigne en estimant que les reproches faits aux consommateurs sont injustifiés`, answerCn: `他感到愤慨，认为对消费者的指责是不公正的` },

          // ── T13 ──
          { type: "section", titleCn: "T13", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 2, topicCn: "", answerFr: `La difficulté à décrire les saveurs`, answerCn: `描述味道的困难` },
          { id: 3, topicCn: "", answerFr: `Instaurer des rapports de réciprocité`, answerCn: `建立互惠关系` },
          { id: 4, topicCn: "", answerFr: `Les intérêts en jeu sont difficilement compatibles`, answerCn: `相关利益难以协调` },
          { id: 5, topicCn: "", answerFr: `La liberté accordée aux visiteurs`, answerCn: `给予访客的自由` },
          { id: 6, topicCn: "", answerFr: `Aborder des œuvres réputées difficiles avec leurs élèves`, answerCn: `与学生一起探讨公认难懂的作品` },

          // ── T14 ──
          { type: "section", titleCn: "T14", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Son charisme incroyable`, answerCn: `他令人难以置信的个人魅力` },
          { id: 2, topicCn: "", answerFr: `Florence a beaucoup de travail`, answerCn: `佛罗伦萨工作繁忙` },
          { id: 3, topicCn: "", answerFr: `Il touche également les adultes`, answerCn: `它同样打动了成年人` },
          { id: 4, topicCn: "", answerFr: `Les financements publics contribuent à leur expansion`, answerCn: `公共资助促进了它们的扩张` },
          { id: 5, topicCn: "", answerFr: `Il constitue un bienfait autant qu'un problème`, answerCn: `它既是一种益处，也是一个问题` },
          { id: 6, topicCn: "", answerFr: `Ses œuvres se fondent dans leur environnement`, answerCn: `他的作品融入其所处的环境` },

          // ── T15 ──
          { type: "section", titleCn: "T15", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科上为自己设定了较高的目标` },
          { id: 2, topicCn: "", answerFr: `Ils sont parfaitement à l'aise avec les derniers outils multimédias`, answerCn: `他们对最新的多媒体工具驾轻就熟` },
          { id: 3, topicCn: "", answerFr: `L'accès réglementé à un emplacement protégé`, answerCn: `对受保护地点的受限访问` },
          { id: 4, topicCn: "", answerFr: `À minimiser les aléas`, answerCn: `将不确定性降到最低` },
          { id: 5, topicCn: "", answerFr: `Parce que l'approvisionnement en électricité est compromis`, answerCn: `因为电力供应受到了影响` },
          { id: 6, topicCn: "", answerFr: `La quasi-absence d'héroïnes`, answerCn: `女主角几乎缺席` },

          // ── T16 ──
          { type: "section", titleCn: "T16", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La méfiance des propriétaires`, answerCn: `业主的不信任` },
          { id: 2, topicCn: "", answerFr: `La sagesse doit l'emporter sur la tentation`, answerCn: `明智应当战胜诱惑` },
          { id: 3, topicCn: "", answerFr: `Ils saisissent toutes les occasions`, answerCn: `他们抓住一切机会` },
          { id: 4, topicCn: "", answerFr: `Instaurer des rapports de réciprocité`, answerCn: `建立互惠关系` },
          { id: 5, topicCn: "", answerFr: `La liberté accordée aux visiteurs`, answerCn: `给予访客的自由` },
          { id: 6, topicCn: "", answerFr: `Il insiste sur le point de vue matériel`, answerCn: `他强调物质层面的观点` },

          // ── T17 ──
          { type: "section", titleCn: "T17", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科上为自己设定了较高的目标` },
          { id: 2, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不受重视的艺术形式` },
          { id: 3, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与对数字世界的探索` },
          { id: 4, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在应当得到官方认可` },
          { id: 5, topicCn: "", answerFr: `Lutter contre elles peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 6, topicCn: "", answerFr: `Aborder des œuvres réputées difficiles avec leurs élèves`, answerCn: `与学生一起探讨公认难懂的作品` },

          // ── T18 ──
          { type: "section", titleCn: "T18", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },
          { id: 2, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多地诉诸理性` },
          { id: 3, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众的对话` },
          { id: 4, topicCn: "", answerFr: `C'est un handicap qui peut se transformer en atout`, answerCn: `这是一种可以转化为优势的劣势` },
          { id: 5, topicCn: "", answerFr: `Attirer l'attention grâce à un coup de publicité`, answerCn: `通过宣传手段吸引眼球` },
          { id: 6, topicCn: "", answerFr: `Ils se détériorent après un certain temps`, answerCn: `它们在一段时间后会退化` },

          // ── T19 ──
          { type: "section", titleCn: "T19", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Son charisme incroyable`, answerCn: `他令人难以置信的个人魅力` },
          { id: 2, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列作品的定期更换` },
          { id: 3, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养他们的批判性思维` },
          { id: 4, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定性` },
          { id: 5, topicCn: "", answerFr: `La liberté accordée aux visiteurs`, answerCn: `给予访客的自由` },
          { id: 6, topicCn: "", answerFr: `Si c'est le fruit d'une décision personnelle`, answerCn: `如果这是个人决定的结果` },

          // ── T20 ──
          { type: "section", titleCn: "T20", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La population est insuffisamment formée aux médias`, answerCn: `民众的媒体素养培训不足` },
          { id: 2, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们颠覆了权威关系` },
          { id: 3, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众的对话` },
          { id: 4, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定性` },
          { id: 5, topicCn: "", answerFr: `Lutter contre elle peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 6, topicCn: "", answerFr: `Si c'est le fruit d'une décision personnelle`, answerCn: `如果这是个人决定的结果` },

          // ── T21 ──
          { type: "section", titleCn: "T21", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Il donne un conseil`, answerCn: `他给出一条建议` },
          { id: 2, topicCn: "", answerFr: `Aider les plus démunis à se loger`, answerCn: `帮助最贫困的人解决住房问题` },
          { id: 3, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定性` },
          { id: 4, topicCn: "", answerFr: `I remet en question des traditions profondément ancrées`, answerCn: `它对根深蒂固的传统提出了质疑` },
          { id: 5, topicCn: "", answerFr: `Lutter contre elles peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 6, topicCn: "", answerFr: `Il insiste sur le pont de vue matériel`, answerCn: `他强调物质层面的观点` },

          // ── T22 ──
          { type: "section", titleCn: "T22", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La technologie facilite le pillage des mers`, answerCn: `技术助长了对海洋的掠夺` },
          { id: 2, topicCn: "", answerFr: `Elle peine à se répandre en milieu professionnel`, answerCn: `它在职业环境中难以普及` },
          { id: 3, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共情` },
          { id: 4, topicCn: "", answerFr: `Leur permettre d'inventer des activités`, answerCn: `让他们能够自创活动` },
          { id: 5, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作机制至今仍是谜` },
          { id: 6, topicCn: "", answerFr: `Ses œuvres se fondent dans leur environnement`, answerCn: `他的作品融入其所处的环境` },

          // ── T23 ──
          { type: "section", titleCn: "T23", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Profiter d'un encadrement spécifique`, answerCn: `利用专项指导框架` },
          { id: 2, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多地诉诸理性` },
          { id: 3, topicCn: "", answerFr: `Les arguments hypocrites avancés par les fabricants`, answerCn: `制造商提出的虚伪论据` },
          { id: 4, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在应当得到官方认可` },
          { id: 5, topicCn: "", answerFr: `Il existerait un ordre universel de la pensée, indépendant de l'ordre linguistique`, answerCn: `存在一种独立于语言秩序的普遍思维秩序` },
          { id: 6, topicCn: "", answerFr: `C'est un vecteur de diffusion des œuvres littéraires`, answerCn: `这是文学作品传播的载体` },

          // ── T24 ──
          { type: "section", titleCn: "T24", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elles captivent l'instantanéité`, answerCn: `它们捕捉瞬间即逝的时刻` },
          { id: 2, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 3, topicCn: "", answerFr: `Instaurer des rapports de réciprocité`, answerCn: `建立互惠关系` },
          { id: 4, topicCn: "", answerFr: `La difficulté d'accéder au sens`, answerCn: `理解意义的困难` },
          { id: 5, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作机制至今仍是谜` },
          { id: 6, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels`, answerCn: `他对传统媒体的价值持怀疑态度` },

          // ── T25 ──
          { type: "section", titleCn: "T25", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elle révèlerait la part de l'acquis due au groupe`, answerCn: `它将揭示群体影响所形成的后天特质` },
          { id: 2, topicCn: "", answerFr: `On veut les préserver durablement`, answerCn: `人们希望对其进行可持续保护` },
          { id: 3, topicCn: "", answerFr: `Il remet en question leurs retombées positives`, answerCn: `他质疑其积极效应` },
          { id: 4, topicCn: "", answerFr: `Lutter contre elles peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 5, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共情` },
          { id: 6, topicCn: "", answerFr: `Simplifier le vocabulaire employé`, answerCn: `简化所用词汇` },

          // ── T26 ──
          { type: "section", titleCn: "T26", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ce sont les violons récents qui sont les plus estimés`, answerCn: `近期制作的小提琴是最受推崇的` },
          { id: 2, topicCn: "", answerFr: `L'accroissement du taux de chômage de ses administrés`, answerCn: `其管辖居民失业率的上升` },
          { id: 3, topicCn: "", answerFr: `Ils saisissent toutes les occasions`, answerCn: `他们抓住一切机会` },
          { id: 4, topicCn: "", answerFr: `Une analyse du contexte socio-éducatif actuel`, answerCn: `对当前社会教育背景的分析` },
          { id: 5, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作机制至今仍是谜` },
          { id: 6, topicCn: "", answerFr: `Aborder des œuvres réputées difficiles avec leurs élèves`, answerCn: `与学生一起探讨公认难懂的作品` },

          // ── T27 ──
          { type: "section", titleCn: "T27", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ce sont les violons récents qui sont les plus estimés`, answerCn: `近期制作的小提琴是最受推崇的` },
          { id: 2, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 3, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养他们的批判性思维` },
          { id: 4, topicCn: "", answerFr: `Il est méconnu du public visé`, answerCn: `它不为目标受众所熟知` },
          { id: 5, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作机制至今仍是谜` },
          { id: 6, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels`, answerCn: `他对传统媒体的价值持怀疑态度` },

          // ── T28 ──
          { type: "section", titleCn: "T28", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `À chaque activité correspond une région précise`, answerCn: `每项活动对应一个特定地区` },
          { id: 2, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列作品的定期更换` },
          { id: 3, topicCn: "", answerFr: `Les financements publics contribuent à leur expansion`, answerCn: `公共资助促进了它们的扩张` },
          { id: 4, topicCn: "", answerFr: `Il est méconnu du public visé`, answerCn: `它不为目标受众所熟知` },
          { id: 5, topicCn: "", answerFr: `Dans un parc naturel`, answerCn: `在一处自然公园中` },
          { id: 6, topicCn: "", answerFr: `Il s'indigne en estimant que les reproches faits aux consommateurs sont injustifiés`, answerCn: `他感到愤慨，认为对消费者的指责是不公正的` },

          // ── T29 ──
          { type: "section", titleCn: "T29", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Le système génétique est affecté`, answerCn: `遗传系统受到了影响` },
          { id: 2, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不受重视的艺术形式` },
          { id: 3, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与对数字世界的探索` },
          { id: 4, topicCn: "", answerFr: `Le risque de saturation des réseaux`, answerCn: `网络饱和的风险` },
          { id: 5, topicCn: "", answerFr: `Une analyse du contexte socio-éducatif actuel`, answerCn: `对当前社会教育背景的分析` },
          { id: 6, topicCn: "", answerFr: `Une grande autonomie dans le domaine professionnel`, answerCn: `在职业领域拥有高度自主性` },

          // ── T30 ──
          { type: "section", titleCn: "T30", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils paraissent manipulés par une force supérieure`, answerCn: `他们似乎被某种更高的力量所操纵` },
          { id: 2, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们颠覆了权威关系` },
          { id: 3, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众的对话` },
          { id: 4, topicCn: "", answerFr: `Ils sont capables de communiquer entre eux`, answerCn: `它们能够相互沟通` },
          { id: 5, topicCn: "", answerFr: `Former les spécialistes du secteur`, answerCn: `培养该领域的专业人才` },
          { id: 6, topicCn: "", answerFr: `Si c'est le fruit d'une décision personnelle`, answerCn: `如果这是个人决定的结果` },

          // ── T31 ──
          { type: "section", titleCn: "T31", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },
          { id: 2, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列作品的定期更换` },
          { id: 3, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定性` },
          { id: 4, topicCn: "", answerFr: `Ils entraînent la disparition de pratiques traditionnelles`, answerCn: `它们导致传统做法的消失` },
          { id: 5, topicCn: "", answerFr: `Ils présentent un partage sexiste des tâches dans le couple`, answerCn: `它们呈现出伴侣间带有性别偏见的分工` },
          { id: 6, topicCn: "", answerFr: `Ils se détériorent après un certain temps`, answerCn: `它们在一段时间后会退化` },

          // ── T32 ──
          { type: "section", titleCn: "T32", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Comme une incitation à l'action`, answerCn: `作为行动的激励` },
          { id: 2, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列作品的定期更换` },
          { id: 3, topicCn: "", answerFr: `Les arguments hypocrites avancés par les fabricants`, answerCn: `制造商提出的虚伪论据` },
          { id: 4, topicCn: "", answerFr: `L'avidité financière des acteurs du secteur touristique`, answerCn: `旅游业从业者的逐利心理` },
          { id: 5, topicCn: "", answerFr: `Attirer l'attention grâce à un coup de publicité`, answerCn: `通过宣传手段吸引眼球` },
          { id: 6, topicCn: "", answerFr: `Une crainte de la hiérarchie quant à la qualité du travail fourni`, answerCn: `管理层对工作质量的顾虑` },

          // ── T33 ──
          { type: "section", titleCn: "T33", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Les réticences émises par la clientèle`, answerCn: `客户所表达的顾虑` },
          { id: 2, topicCn: "", answerFr: `La 200e édition d'une émission`, answerCn: `某节目的第200期` },
          { id: 3, topicCn: "", answerFr: `Elle s'abstrait un temps de ses soucis`, answerCn: `她暂时从忧虑中抽离出来` },
          { id: 4, topicCn: "", answerFr: `Pour sortir de la crise que son économie subissait`, answerCn: `为了摆脱其经济所遭受的危机` },
          { id: 5, topicCn: "", answerFr: `La mise en place de la démocratie résulte d'un long processus`, answerCn: `民主制度的建立是一个漫长过程的结果` },
          { id: 6, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels`, answerCn: `他对传统媒体的价值持怀疑态度` },

          // ── T34 ──
          { type: "section", titleCn: "T34", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Permet de découvrir les saveurs antillaises`, answerCn: `让人发现安的列斯群岛的风味` },
          { id: 2, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不受重视的艺术形式` },
          { id: 3, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养他们的批判性思维` },
          { id: 4, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在应当得到官方认可` },
          { id: 5, topicCn: "", answerFr: `Dans un parc naturel`, answerCn: `在一处自然公园中` },
          { id: 6, topicCn: "", answerFr: `Parce que l'approvisionnement en électricité est compromis`, answerCn: `因为电力供应受到了影响` },

          // ── T35 ──
          { type: "section", titleCn: "T35", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils sont capables de se reconnaître entre eux`, answerCn: `它们能够相互识别` },
          { id: 2, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们颠覆了权威关系` },
          { id: 3, topicCn: "", answerFr: `Il met à jour un enfermement ignoré`, answerCn: `它揭示了一种被忽视的禁锢状态` },
          { id: 4, topicCn: "", answerFr: `La difficulté d'accéder au sens`, answerCn: `理解意义的困难` },
          { id: 5, topicCn: "", answerFr: `L'avidité financière des acteurs du secteur touristique`, answerCn: `旅游业从业者的逐利心理` },
          { id: 6, topicCn: "", answerFr: `L'auteur a imaginé différents scénarios`, answerCn: `作者设想了不同的场景` },

          // ── T36 ──
          { type: "section", titleCn: "T36", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Elles sont issues de techniques variées`, answerCn: `它们源自各种不同的技术` },
          { id: 2, topicCn: "", answerFr: `À l'enrichissement du lexique`, answerCn: `对词汇的丰富` },
          { id: 3, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共情` },
          { id: 4, topicCn: "", answerFr: `Ils sont capables de communiquer entre eux`, answerCn: `它们能够相互沟通` },
          { id: 5, topicCn: "", answerFr: `De satisfaire avant tout les adultes`, answerCn: `首先要满足成年人的需求` },
          { id: 6, topicCn: "", answerFr: `En abandonnant les codes traditionnels du roman`, answerCn: `摒弃小说的传统规范` },

          // ── T37 ──
          { type: "section", titleCn: "T37", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科上为自己设定了较高的目标` },
          { id: 2, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多地诉诸理性` },
          { id: 3, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与对数字世界的探索` },
          { id: 4, topicCn: "", answerFr: `Leur permettre d'inventer des activités`, answerCn: `让他们能够自创活动` },
          { id: 5, topicCn: "", answerFr: `Former les spécialistes du secteur`, answerCn: `培养该领域的专业人才` },
          { id: 6, topicCn: "", answerFr: `À minimiser les aléas`, answerCn: `将不确定性降到最低` },

          // ── T38 ──
          { type: "section", titleCn: "T38", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Mémoriser des concepts sans les comprendre`, answerCn: `在不理解的情况下死记概念` },
          { id: 2, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们颠覆了权威关系` },
          { id: 3, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养他们的批判性思维` },
          { id: 4, topicCn: "", answerFr: `Le risque de saturation des réseaux`, answerCn: `网络饱和的风险` },
          { id: 5, topicCn: "", answerFr: `Former les spécialistes du secteur`, answerCn: `培养该领域的专业人才` },
          { id: 6, topicCn: "", answerFr: `Ses œuvres se fondent dans leur environnement`, answerCn: `他的作品融入其所处的环境` },

          // ── T39 ──
          { type: "section", titleCn: "T39", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Demander à une cliente de payer l'intégralité de sa commande`, answerCn: `要求顾客全额支付订单` },
          { id: 2, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 3, topicCn: "", answerFr: `Les arguments hypocrites avancés par les fabricants`, answerCn: `制造商提出的虚伪论据` },
          { id: 4, topicCn: "", answerFr: `C'est un handicap qui peut se transformer en atout`, answerCn: `这是一种可以转化为优势的劣势` },
          { id: 5, topicCn: "", answerFr: `La mise en place de la démocratie résulte d'un long processus`, answerCn: `民主制度的建立是一个漫长过程的结果` },
          { id: 6, topicCn: "", answerFr: `Ils se détériorent après un certain temps`, answerCn: `它们在一段时间后会退化` },

          // ── T40 ──
          { type: "section", titleCn: "T40", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `La population est insuffisamment formée aux médias`, answerCn: `民众的媒体素养培训不足` },
          { id: 2, topicCn: "", answerFr: `Elle peine à se répandre en milieu professionnel`, answerCn: `它在职业环境中难以普及` },
          { id: 3, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养他们的批判性思维` },
          { id: 4, topicCn: "", answerFr: `Il nuance les prévisions alarmistes`, answerCn: `他对悲观预测进行了修正` },
          { id: 5, topicCn: "", answerFr: `Elles bénéficient d'un effet de mode`, answerCn: `它们得益于时尚效应` },
          { id: 6, topicCn: "", answerFr: `Il se sentait trop vieux pour les tournées`, answerCn: `他觉得自己年纪太大，不适合巡演了` },

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
