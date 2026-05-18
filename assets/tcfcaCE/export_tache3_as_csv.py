#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
[
       { type: "section", titleCn: "T1", descFr: "", descCn: "" },
          { id: 1, topicCn: "", answerFr: `Le système génétique est affecté`, answerCn: `遗传系统受到影响` },
          { id: 2, topicCn: "", answerFr: `L'absence totale des signes visuels du langage`, answerCn: `语言视觉符号完全缺失` },
          { id: 3, topicCn: "", answerFr: `Si on modifie la façon dont on les perçoit`, answerCn: `如果改变我们看待它们的方式` },
          { id: 4, topicCn: "", answerFr: `Le déroulement des événements`, answerCn: `事件的发展过程` },
          { id: 5, topicCn: "", answerFr: `Ils présentent un partage sexiste des tâches dans le couple`, answerCn: `伴侣关系中的性别化分工` },
          { id: 6, topicCn: "", answerFr: `Il existerait un ordre universel de la pensée indépendant de l'ordre linguistique`, answerCn: `思想可能存在独立于语言秩序的普遍结构` },

          { type: "section", titleCn: "T2", descFr: "", descCn: "" },
          { id: 7, topicCn: "", answerFr: `La méfiance des propriétaires`, answerCn: `房东的不信任` },
          { id: 8, topicCn: "", answerFr: `L'accès réglementé à un emplacement protégé`, answerCn: `进入受保护地点受到限制` },
          { id: 9, topicCn: "", answerFr: `L'absence de prise de décisions effectives`, answerCn: `缺乏有效决策` },
          { id: 10, topicCn: "", answerFr: `Elle permet le dépassement des normes édictées`, answerCn: `它允许突破既定规范` },
          { id: 11, topicCn: "", answerFr: `L'extension d'un système de climatisation à tout un quartier`, answerCn: `将空调系统扩展到整个街区` },
          { id: 12, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels`, answerCn: `他怀疑传统媒体的价值` },

          { type: "section", titleCn: "T3", descFr: "", descCn: "" },
          { id: 13, topicCn: "", answerFr: `Il donne un conseil`, answerCn: `他提出一个建议` },
          { id: 14, topicCn: "", answerFr: `Les réticences émises par la clientèle`, answerCn: `顾客提出的顾虑` },
          { id: 15, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共鸣` },
          { id: 16, topicCn: "", answerFr: `Les intérêts en jeu sont difficilement compatibles`, answerCn: `涉及的利益难以兼容` },
          { id: 17, topicCn: "", answerFr: `Donner une dimension nouvelle aux lieux mis en scène`, answerCn: `为呈现的场所赋予新的维度` },
          { id: 18, topicCn: "", answerFr: `À minimiser les aléas`, answerCn: `减少不确定性` },

          { type: "section", titleCn: "T4", descFr: "", descCn: "" },
          { id: 19, topicCn: "", answerFr: `La méfiance des propriétaires`, answerCn: `房东的不信任` },
          { id: 20, topicCn: "", answerFr: `Permettre aux jeunes de découvrir un sport difficile`, answerCn: `让年轻人发现一项困难的运动` },
          { id: 21, topicCn: "", answerFr: `Il se réfugiait dans le dessin pour échapper à ses camarades`, answerCn: `他通过画画来躲避同学` },
          { id: 22, topicCn: "", answerFr: `Diffuser l'art dans des endroits inattendus`, answerCn: `在意想不到的地方传播艺术` },
          { id: 23, topicCn: "", answerFr: `Le déroulement des événements`, answerCn: `事件的发展过程` },
          { id: 24, topicCn: "", answerFr: `En abandonnant les codes traditionnels du roman`, answerCn: `通过放弃传统小说的规范` },

          { type: "section", titleCn: "T5", descFr: "", descCn: "" },
          { id: 25, topicCn: "", answerFr: `Permet de découvrir les saveurs antillaises`, answerCn: `发现安的列斯群岛风味` },
          { id: 26, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多诉诸理性` },
          { id: 27, topicCn: "", answerFr: `Pour sortir de la crise que son économie subissait`, answerCn: `摆脱其经济危机` },
          { id: 28, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在必须被正式承认` },
          { id: 29, topicCn: "", answerFr: `Une analyse du contexte socio-éducatif actuel`, answerCn: `当前社会教育背景分析` },
          { id: 30, topicCn: "", answerFr: `La singularité de ses portraits`, answerCn: `其肖像作品的独特性` },

          { type: "section", titleCn: "T6", descFr: "", descCn: "" },
          { id: 31, topicCn: "", answerFr: `L'utilisation abusive de flashbacks`, answerCn: `过度使用倒叙` },
          { id: 32, topicCn: "", answerFr: `La 200e édition d'une émission`, answerCn: `节目第200期` },
          { id: 33, topicCn: "", answerFr: `Il a du mal à se déplacer dans la foule`, answerCn: `在人群中行动困难` },
          { id: 34, topicCn: "", answerFr: `Exploiter les compétences acquises`, answerCn: `利用获得的能力` },
          { id: 35, topicCn: "", answerFr: `Ils présentent un partage sexiste des tâches dans le couple`, answerCn: `伴侣关系中的性别分工` },
          { id: 36, topicCn: "", answerFr: `Il se sentait trop vieux pour les tournées`, answerCn: `觉得自己太老不适合巡演` },

          { type: "section", titleCn: "T7", descFr: "", descCn: "" },
          { id: 37, topicCn: "", answerFr: `Un couple qui ne s'aime plus`, answerCn: `一对不再相爱的夫妻` },
          { id: 38, topicCn: "", answerFr: `En s'enrichissant de tous types d'apports`, answerCn: `通过吸收各种来源的贡献而丰富` },
          { id: 39, topicCn: "", answerFr: `Il est indispensable de savoir s'en servir correctement`, answerCn: `必须懂得正确使用它` },
          { id: 40, topicCn: "", answerFr: `Elle répond à certaines règles compréhensibles`, answerCn: `它遵循一些可以理解的规则` },
          { id: 41, topicCn: "", answerFr: `Le déroulement des événements`, answerCn: `事件的发展过程` },
          { id: 42, topicCn: "", answerFr: `De satisfaire avant tout les adultes`, answerCn: `首先满足成年人` },

          { type: "section", titleCn: "T8", descFr: "", descCn: "" },
          { id: 43, topicCn: "", answerFr: `Elle doit se fonder sur l'estime mutuelle`, answerCn: `它必须建立在相互尊重的基础上` },
          { id: 44, topicCn: "", answerFr: `L'absence totale des signes visuels du langage`, answerCn: `语言视觉符号完全缺失` },
          { id: 45, topicCn: "", answerFr: `Pour sortir de la crise que son économie subissait`, answerCn: `为了摆脱其经济危机` },
          { id: 46, topicCn: "", answerFr: `La société actuelle accepte mal qu'un enfant élevé uniquement par son père`, answerCn: `现代社会难以接受只由父亲抚养的孩子` },
          { id: 47, topicCn: "", answerFr: `Il existerait un ordre universel de la pensée indépendant de l'ordre linguistique`, answerCn: `思想可能存在独立于语言秩序的普遍结构` },
          { id: 48, topicCn: "", answerFr: `De satisfaire avant tout les adultes`, answerCn: `首先满足成年人` },

          { type: "section", titleCn: "T9", descFr: "", descCn: "" },
          { id: 49, topicCn: "", answerFr: `Profiter d'un encadrement spécifique`, answerCn: `利用特定指导` },
          { id: 50, topicCn: "", answerFr: `Son charisme incroyable`, answerCn: `他惊人的魅力` },
          { id: 51, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与数字世界的探索` },
          { id: 52, topicCn: "", answerFr: `Diffuser l'art dans des endroits inattendus`, answerCn: `在意想不到的地方传播艺术` },
          { id: 53, topicCn: "", answerFr: `Dans un parc naturel`, answerCn: `在一个自然公园中` },
          { id: 54, topicCn: "", answerFr: `Il insiste sur le point de vue matériel`, answerCn: `他强调物质层面的观点` },

          { type: "section", titleCn: "T10", descFr: "", descCn: "" },
          { id: 55, topicCn: "", answerFr: `Demande à une cliente de payer l’intégralité de sa commande`, answerCn: `要求一位女顾客支付她订单的全部金额` },
          { id: 56, topicCn: "", answerFr: `Des passionnés de randonnée`, answerCn: `一些热爱徒步旅行的人` },
          { id: 57, topicCn: "", answerFr: `Il était déjà, en son temps, un artiste reconnu par ses pairs`, answerCn: `在他那个时代，他就已经是一位得到同行认可的艺术家` },
          { id: 58, topicCn: "", answerFr: `C’est un marqueur social`, answerCn: `这是一个社会地位标志` },
          { id: 59, topicCn: "", answerFr: `La société actuelle accepte mal qu’un enfant élevé uniquement par son père`, answerCn: `当今社会不太能接受一个孩子仅由父亲抚养长大` },
          { id: 60, topicCn: "", answerFr: `Le raisonnement du penseur représente une entrave à la création`, answerCn: `这位思想家的推理构成了创作的阻碍` },

          { type: "section", titleCn: "T11", descFr: "", descCn: "" },
          { id: 61, topicCn: "", answerFr: `La rivalité entre les différents médias`, answerCn: `不同媒体之间的竞争` },
          { id: 62, topicCn: "", answerFr: `Les réticences émises par la clientèle`, answerCn: `顾客提出的顾虑` },
          { id: 63, topicCn: "", answerFr: `Les financements publics contribuent à leur expansion`, answerCn: `公共资金促进其扩张` },
          { id: 64, topicCn: "", answerFr: `Elle permet le dépassement des normes édictées`, answerCn: `它使人们能够突破既定规范` },
          { id: 65, topicCn: "", answerFr: `La mise en place de la démocratie résulte d'un long processus`, answerCn: `民主的建立源于一个漫长的过程` },
          { id: 66, topicCn: "", answerFr: `Il insiste sur le point de vue matériel`, answerCn: `他强调物质层面的观点` },

          { type: "section", titleCn: "T12", descFr: "", descCn: "" },
          { id: 67, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科中设定很高的目标` },
          { id: 68, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不被重视的艺术形式` },
          { id: 69, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众对话` },
          { id: 70, topicCn: "", answerFr: `Elle permet le dépassement des normes édictées`, answerCn: `它允许突破既定规范` },
          { id: 71, topicCn: "", answerFr: `L'extension d'un système de climatisation à tout un quartier.`, answerCn: `将空调系统扩展到整个街区。` },
          { id: 72, topicCn: "", answerFr: `Il s'indigne en estimant que les reproches faits aux consommateurs sont injustifiés.`, answerCn: `他愤怒地认为对消费者的指责是不合理的。` },

          { type: "section", titleCn: "T13", descFr: "", descCn: "" },
          { id: 73, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 74, topicCn: "", answerFr: `La difficulté à décrire les saveurs`, answerCn: `难以描述味道` },
          { id: 75, topicCn: "", answerFr: `Instaurer des rapports de réciprocité`, answerCn: `建立互惠关系` },
          { id: 76, topicCn: "", answerFr: `Les intérêts en jeu sont difficilement compatibles`, answerCn: `涉及的利益难以兼容` },
          { id: 77, topicCn: "", answerFr: `La liberté accordée aux visiteurs`, answerCn: `给予游客的自由` },
          { id: 78, topicCn: "", answerFr: `Aborder des œuvres réputées difficiles avec leurs élèves`, answerCn: `与学生一起研究被认为困难的作品` },

          { type: "section", titleCn: "T14", descFr: "", descCn: "" },
          { id: 79, topicCn: "", answerFr: `Son charisme incroyable`, answerCn: `他惊人的魅力` },
          { id: 80, topicCn: "", answerFr: `Florence a beaucoup de travail`, answerCn: `Florence 有很多工作` },
          { id: 81, topicCn: "", answerFr: `Il touche également les adultes`, answerCn: `它同样影响成年人` },
          { id: 82, topicCn: "", answerFr: `Les financements publics contribuent à leur expansion`, answerCn: `公共资金促进其扩张` },
          { id: 83, topicCn: "", answerFr: `Il constitue un bienfait autant qu'un problème`, answerCn: `它既是好处也是问题` },
          { id: 84, topicCn: "", answerFr: `Ses œuvres se fondent dans leur environnement`, answerCn: `他的作品融入其环境` },

          { type: "section", titleCn: "T15", descFr: "", descCn: "" },
          { id: 85, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科中设定高目标` },
          { id: 86, topicCn: "", answerFr: `Ils sont parfaitement à l'aise avec les derniers outils multimédias`, answerCn: `他们熟练使用最新多媒体工具` },
          { id: 87, topicCn: "", answerFr: `L'accès réglementé à un emplacement protégé`, answerCn: `进入受保护地点受到限制` },
          { id: 88, topicCn: "", answerFr: `À minimiser les aléas`, answerCn: `减少不确定性` },
          { id: 89, topicCn: "", answerFr: `Parce que l'approvisionnement en électricité est compromis`, answerCn: `因为电力供应受到影响` },
          { id: 90, topicCn: "", answerFr: `La quasi-absence d'héroïnes`, answerCn: `女性角色几乎缺失` },

          { type: "section", titleCn: "T16", descFr: "", descCn: "" },
          { id: 91, topicCn: "", answerFr: `La méfiance des propriétaires`, answerCn: `房东的不信任` },
          { id: 92, topicCn: "", answerFr: `La sagesse doit l'emporter sur la tentation`, answerCn: `理性必须战胜诱惑` },
          { id: 93, topicCn: "", answerFr: `Ils saisissent toutes les occasions`, answerCn: `他们抓住一切机会` },
          { id: 94, topicCn: "", answerFr: `Instaurer des rapports de réciprocité`, answerCn: `建立互惠关系` },
          { id: 95, topicCn: "", answerFr: `La liberté accordée aux visiteurs`, answerCn: `给予游客的自由` },
          { id: 96, topicCn: "", answerFr: `Il insiste sur le point de vue matériel`, answerCn: `他强调物质层面的观点` },

          { type: "section", titleCn: "T17", descFr: "", descCn: "" },
          { id: 97, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科中设定高目标` },
          { id: 98, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不被重视的艺术形式` },
          { id: 99, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与数字世界探索` },
          { id: 100, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在必须被正式确认` },
          { id: 101, topicCn: "", answerFr: `Lutter contre elles peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 102, topicCn: "", answerFr: `Aborder des œuvres réputées difficiles avec leurs élèves.`, answerCn: `与学生一起研究被认为困难的作品。` },

          { type: "section", titleCn: "T18", descFr: "", descCn: "" },
          { id: 103, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },
          { id: 104, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多诉诸理性` },
          { id: 105, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众对话` },
          { id: 106, topicCn: "", answerFr: `C'est un handicap qui peut se transformer en atout`, answerCn: `这是一种可以转化为优势的劣势` },
          { id: 107, topicCn: "", answerFr: `Attirer l'attention grâce à un coup de publicité`, answerCn: `通过宣传吸引注意` },
          { id: 108, topicCn: "", answerFr: `Ils se détériorent après un certain temps`, answerCn: `它们在一段时间后会恶化` },

          { type: "section", titleCn: "T19", descFr: "", descCn: "" },
          { id: 109, topicCn: "", answerFr: `Son charisme incroyable`, answerCn: `他惊人的魅力` },
          { id: 110, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列的定期更换` },
          { id: 111, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养批判性思维` },
          { id: 112, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定` },
          { id: 113, topicCn: "", answerFr: `La liberté accordée aux visiteurs`, answerCn: `给予游客的自由` },
          { id: 114, topicCn: "", answerFr: `Si c'est le fruit d'une décision personnelle`, answerCn: `如果这是个人决定的结果` },

          { type: "section", titleCn: "T20", descFr: "", descCn: "" },
          { id: 115, topicCn: "", answerFr: `La population est insuffisamment formée aux médias`, answerCn: `公众媒体素养不足` },
          { id: 116, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们改变权威关系` },
          { id: 117, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众对话` },
          { id: 118, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定` },
          { id: 119, topicCn: "", answerFr: `Lutter contre elles peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 120, topicCn: "", answerFr: `Si c'est le fruit d'une décision personnelle`, answerCn: `如果这是个人决定的结果` },

          { type: "section", titleCn: "T21", descFr: "", descCn: "" },
          { id: 121, topicCn: "", answerFr: `Il donne un conseil`, answerCn: `他提出一个建议` },
          { id: 122, topicCn: "", answerFr: `Aider les plus démunis à se loger`, answerCn: `帮助最贫困的人找到住房` },
          { id: 123, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定` },
          { id: 124, topicCn: "", answerFr: `Il remet en question des traditions profondément ancrées`, answerCn: `他质疑根深蒂固的传统` },
          { id: 125, topicCn: "", answerFr: `Lutter contre elles peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 126, topicCn: "", answerFr: `Il insiste sur le point de vue matériel`, answerCn: `他强调物质层面的观点` },

          { type: "section", titleCn: "T22", descFr: "", descCn: "" },
          { id: 127, topicCn: "", answerFr: `La technologie facilite le pillage des mers`, answerCn: `技术使海洋掠夺更容易` },
          { id: 128, topicCn: "", answerFr: `Elle peine à se répandre en milieu professionnel`, answerCn: `它在职业环境中难以传播` },
          { id: 129, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共鸣` },
          { id: 130, topicCn: "", answerFr: `Leur permettre d'inventer des activités`, answerCn: `让他们创造新的活动` },
          { id: 131, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作仍然神秘` },
          { id: 132, topicCn: "", answerFr: `Ses œuvres se fondent dans leur environnement`, answerCn: `他的作品融入其环境` },

          { type: "section", titleCn: "T23", descFr: "", descCn: "" },
          { id: 133, topicCn: "", answerFr: `Profiter d'un encadrement spécifique`, answerCn: `利用特定指导` },
          { id: 134, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多诉诸理性` },
          { id: 135, topicCn: "", answerFr: `Les arguments hypocrites avancés par les fabricants`, answerCn: `制造商提出的虚伪论点` },
          { id: 136, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在必须被正式确认` },
          { id: 137, topicCn: "", answerFr: `Il existerait un ordre universel de la pensée indépendant de l'ordre linguistique`, answerCn: `思想可能存在独立于语言秩序的普遍结构` },
          { id: 138, topicCn: "", answerFr: `C'est un vecteur de diffusion des œuvres littéraires.`, answerCn: `它是传播文学作品的一种媒介。` },

          { type: "section", titleCn: "T24", descFr: "", descCn: "" },
          { id: 139, topicCn: "", answerFr: `Elles captivent l'instantanéité`, answerCn: `它们捕捉瞬间` },
          { id: 140, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 141, topicCn: "", answerFr: `Instaurer des rapports de réciprocité`, answerCn: `建立互惠关系` },
          { id: 142, topicCn: "", answerFr: `La difficulté d'accéder au sens`, answerCn: `理解意义的困难` },
          { id: 143, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作仍然神秘` },
          { id: 144, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels`, answerCn: `他怀疑传统媒体的价值` },

          { type: "section", titleCn: "T25", descFr: "", descCn: "" },
          { id: 145, topicCn: "", answerFr: `Elle révélerait la part de l'acquis due au groupe`, answerCn: `它揭示群体带来的习得部分` },
          { id: 146, topicCn: "", answerFr: `On veut les préserver durablement`, answerCn: `人们希望长期保护它们` },
          { id: 147, topicCn: "", answerFr: `Il remet en question leurs retombées positives`, answerCn: `他质疑其积极影响` },
          { id: 148, topicCn: "", answerFr: `Lutter contre elles peut nuire à certaines libertés`, answerCn: `与之对抗可能损害某些自由` },
          { id: 149, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共鸣` },
          { id: 150, topicCn: "", answerFr: `Simplifier le vocabulaire employé`, answerCn: `简化使用的词汇` },

          { type: "section", titleCn: "T26", descFr: "", descCn: "" },
          { id: 151, topicCn: "", answerFr: `Ce sont les violons récents qui sont les plus estimés`, answerCn: `最近制作的小提琴最受重视` },
          { id: 152, topicCn: "", answerFr: `L'accroissement du taux de chômage de ses administrés`, answerCn: `其管辖区域失业率上升` },
          { id: 153, topicCn: "", answerFr: `Ils saisissent toutes les occasions`, answerCn: `他们抓住一切机会` },
          { id: 154, topicCn: "", answerFr: `Une analyse du contexte socio-éducatif actuel`, answerCn: `对当前社会教育背景的分析` },
          { id: 155, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作仍然神秘` },
          { id: 156, topicCn: "", answerFr: `Aborder des œuvres réputées difficiles avec leurs élèves`, answerCn: `与学生一起研究被认为困难的作品` },

          { type: "section", titleCn: "T27", descFr: "", descCn: "" },
          { id: 157, topicCn: "", answerFr: `Ce sont les violons récents qui sont les plus estimés`, answerCn: `最近制作的小提琴最受重视` },
          { id: 158, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 159, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养批判性思维` },
          { id: 160, topicCn: "", answerFr: `Il est méconnu du public visé`, answerCn: `目标公众对它了解不多` },
          { id: 161, topicCn: "", answerFr: `Son fonctionnement est encore mystérieux`, answerCn: `它的运作仍然神秘` },
          { id: 162, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels`, answerCn: `他怀疑传统媒体的价值` },

          { type: "section", titleCn: "T28", descFr: "", descCn: "" },
          { id: 163, topicCn: "", answerFr: `À chaque activité correspond une région précise`, answerCn: `每项活动对应一个特定地区` },
          { id: 164, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列的定期更换` },
          { id: 165, topicCn: "", answerFr: `Les financements publics contribuent à leur expansion`, answerCn: `公共资金促进其扩张` },
          { id: 166, topicCn: "", answerFr: `Il est méconnu du public visé.`, answerCn: `目标公众对它了解不多。` },
          { id: 167, topicCn: "", answerFr: `Dans un parc naturel.`, answerCn: `在一个自然公园里。` },
          { id: 168, topicCn: "", answerFr: `Il s'indigne en estimant que les reproches faits aux consommateurs sont injustifiés.`, answerCn: `他愤怒地认为对消费者的指责是不合理的。` },

          { type: "section", titleCn: "T29", descFr: "", descCn: "" },
          { id: 169, topicCn: "", answerFr: `Le système génétique est affecté`, answerCn: `遗传系统受到影响` },
          { id: 170, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不被重视的艺术形式` },
          { id: 171, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与数字世界探索` },
          { id: 172, topicCn: "", answerFr: `Le risque de saturation des réseaux`, answerCn: `网络过载风险` },
          { id: 173, topicCn: "", answerFr: `Une analyse du contexte socio-éducatif actuel`, answerCn: `对当前社会教育背景的分析` },
          { id: 174, topicCn: "", answerFr: `Une grande autonomie dans le domaine professionnel`, answerCn: `职业领域高度自主` },

          { type: "section", titleCn: "T30", descFr: "", descCn: "" },
          { id: 175, topicCn: "", answerFr: `Ils paraissent manipulés par une force supérieure`, answerCn: `他们似乎被某种更高力量操控` },
          { id: 176, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们改变权威关系` },
          { id: 177, topicCn: "", answerFr: `Encourager le dialogue avec le public`, answerCn: `鼓励与公众对话` },
          { id: 178, topicCn: "", answerFr: `Ils sont capables de communiquer entre eux`, answerCn: `它们能够彼此沟通` },
          { id: 179, topicCn: "", answerFr: `Former les spécialistes du secteur`, answerCn: `培养该领域专家` },
          { id: 180, topicCn: "", answerFr: `Si c'est le fruit d'une décision personnelle`, answerCn: `如果这是个人决定的结果` },

          { type: "section", titleCn: "T31", descFr: "", descCn: "" },
          { id: 181, topicCn: "", answerFr: `L'innovation des procédés de production`, answerCn: `生产工艺的创新` },
          { id: 182, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列的定期更换` },
          { id: 183, topicCn: "", answerFr: `La précarité du monde professionnel`, answerCn: `职业世界的不稳定` },
          { id: 184, topicCn: "", answerFr: `Ils entraînent la disparition de pratiques traditionnelles`, answerCn: `它们导致传统做法消失` },
          { id: 185, topicCn: "", answerFr: `Ils présentent un partage sexiste des tâches dans le couple`, answerCn: `伴侣关系中的性别分工` },
          { id: 186, topicCn: "", answerFr: `Ils se détériorent après un certain temps`, answerCn: `它们在一段时间后会恶化` },

          { type: "section", titleCn: "T32", descFr: "", descCn: "" },
          { id: 187, topicCn: "", answerFr: `Comme une incitation à l'action`, answerCn: `作为行动的激励` },
          { id: 188, topicCn: "", answerFr: `Le changement régulier des séries`, answerCn: `系列的定期更换` },
          { id: 189, topicCn: "", answerFr: `Les arguments hypocrites avancés par les fabricants`, answerCn: `制造商提出的虚伪论点` },
          { id: 190, topicCn: "", answerFr: `L'avidité financière des acteurs du secteur touristique`, answerCn: `旅游业从业者的贪婪` },
          { id: 191, topicCn: "", answerFr: `Attirer l'attention grâce à un coup de publicité`, answerCn: `通过宣传吸引注意` },
          { id: 192, topicCn: "", answerFr: `Une crainte de la hiérarchie quant à la qualité du travail fourni`, answerCn: `管理层担心工作质量` },

          { type: "section", titleCn: "T33", descFr: "", descCn: "" },
          { id: 193, topicCn: "", answerFr: `Les réticences émises par la clientèle`, answerCn: `顾客提出的顾虑` },
          { id: 194, topicCn: "", answerFr: `La 200e édition d'une émission`, answerCn: `节目第200期` },
          { id: 195, topicCn: "", answerFr: `Elle s'abstrait un temps de ses soucis`, answerCn: `她暂时摆脱烦恼` },
          { id: 196, topicCn: "", answerFr: `Pour sortir de la crise que son économie subissait`, answerCn: `为了摆脱经济危机` },
          { id: 197, topicCn: "", answerFr: `La mise en place de la démocratie résulte d'un long processus.`, answerCn: `民主制度的建立源于一个漫长的过程。` },
          { id: 198, topicCn: "", answerFr: `Il doute de l'intérêt des médias traditionnels.`, answerCn: `他怀疑传统媒体的价值。` },

          { type: "section", titleCn: "T34", descFr: "", descCn: "" },
          { id: 199, topicCn: "", answerFr: `Permet de découvrir les saveurs antillaises`, answerCn: `发现安的列斯群岛风味` },
          { id: 200, topicCn: "", answerFr: `C'est la photographie qui est la forme d'art la moins valorisée`, answerCn: `摄影是最不被重视的艺术形式` },
          { id: 201, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养批判性思维` },
          { id: 202, topicCn: "", answerFr: `Son existence doit être officialisée`, answerCn: `其存在必须被正式确认` },
          { id: 203, topicCn: "", answerFr: `Dans un parc naturel`, answerCn: `在自然公园中` },
          { id: 204, topicCn: "", answerFr: `Parce que l'approvisionnement en électricité est compromis`, answerCn: `因为电力供应受到影响` },

          { type: "section", titleCn: "T35", descFr: "", descCn: "" },
          { id: 205, topicCn: "", answerFr: `Ils sont capables de se reconnaître entre eux`, answerCn: `他们能够彼此识别` },
          { id: 206, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们改变权威关系` },
          { id: 207, topicCn: "", answerFr: `Il met à jour un enfermement ignoré`, answerCn: `他揭示了被忽视的束缚` },
          { id: 208, topicCn: "", answerFr: `La difficulté d'accéder au sens`, answerCn: `理解意义的困难` },
          { id: 209, topicCn: "", answerFr: `L'avidité financière des acteurs du secteur touristique`, answerCn: `旅游业从业者的贪婪` },
          { id: 210, topicCn: "", answerFr: `L'auteur a imaginé différents scénarios`, answerCn: `作者设想了不同情境` },

          { type: "section", titleCn: "T36", descFr: "", descCn: "" },
          { id: 211, topicCn: "", answerFr: `Elles sont issues de techniques variées`, answerCn: `它们来自多种技术` },
          { id: 212, topicCn: "", answerFr: `À l'enrichissement du lexique`, answerCn: `丰富词汇` },
          { id: 213, topicCn: "", answerFr: `Amener les spectateurs à s'émouvoir d'un quotidien douloureux`, answerCn: `让观众对痛苦的日常生活产生共鸣` },
          { id: 214, topicCn: "", answerFr: `Ils sont capables de communiquer entre eux`, answerCn: `它们能够彼此沟通` },
          { id: 215, topicCn: "", answerFr: `De satisfaire avant tout les adultes`, answerCn: `首先满足成年人` },
          { id: 216, topicCn: "", answerFr: `En abandonnant les codes traditionnels du roman`, answerCn: `通过放弃传统小说规范` },

          { type: "section", titleCn: "T37", descFr: "", descCn: "" },
          { id: 217, topicCn: "", answerFr: `Ils se fixent des objectifs élevés dans ces matières`, answerCn: `他们在这些学科中设定高目标` },
          { id: 218, topicCn: "", answerFr: `De solliciter davantage la raison`, answerCn: `更多诉诸理性` },
          { id: 219, topicCn: "", answerFr: `De participer à l'exploration du monde numérique`, answerCn: `参与数字世界探索` },
          { id: 220, topicCn: "", answerFr: `Leur permettre d'inventer des activités`, answerCn: `让他们创造新的活动` },
          { id: 221, topicCn: "", answerFr: `Former les spécialistes du secteur`, answerCn: `培养该领域专家` },
          { id: 222, topicCn: "", answerFr: `À minimiser les aléas`, answerCn: `减少不确定性` },

          { type: "section", titleCn: "T38", descFr: "", descCn: "" },
          { id: 223, topicCn: "", answerFr: `Mémoriser des concepts sans les comprendre`, answerCn: `记住概念却不理解` },
          { id: 224, topicCn: "", answerFr: `Ils bouleversent les rapports d'autorité`, answerCn: `它们改变权威关系` },
          { id: 225, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养批判性思维` },
          { id: 226, topicCn: "", answerFr: `Le risque de saturation des réseaux`, answerCn: `网络过载风险` },
          { id: 227, topicCn: "", answerFr: `Former les spécialistes du secteur`, answerCn: `培养该领域专家` },
          { id: 228, topicCn: "", answerFr: `Ses œuvres se fondent dans leur environnement`, answerCn: `他的作品融入其环境` },

          { type: "section", titleCn: "T39", descFr: "", descCn: "" },
          { id: 229, topicCn: "", answerFr: `Demander à une cliente de payer l'intégralité de sa commande`, answerCn: `要求顾客支付全部订单金额` },
          { id: 230, topicCn: "", answerFr: `Sur la pollution atmosphérique`, answerCn: `关于大气污染` },
          { id: 231, topicCn: "", answerFr: `Les arguments hypocrites avancés par les fabricants`, answerCn: `制造商提出的虚伪论点` },
          { id: 232, topicCn: "", answerFr: `C'est un handicap qui peut se transformer en atout`, answerCn: `这是一种可以转化为优势的劣势` },
          { id: 233, topicCn: "", answerFr: `La mise en place de la démocratie résulte d'un long processus`, answerCn: `民主的建立源于漫长过程` },
          { id: 234, topicCn: "", answerFr: `Ils se détériorent après un certain temps`, answerCn: `它们在一段时间后会恶化` },

          { type: "section", titleCn: "T40", descFr: "", descCn: "" },
          { id: 235, topicCn: "", answerFr: `La population est insuffisamment formée aux médias`, answerCn: `公众媒体素养不足` },
          { id: 236, topicCn: "", answerFr: `Elle peine à se répandre en milieu professionnel`, answerCn: `在职业环境中难以传播` },
          { id: 237, topicCn: "", answerFr: `Développer leur esprit critique`, answerCn: `培养批判性思维` },
          { id: 238, topicCn: "", answerFr: `Il nuance les prévisions alarmistes`, answerCn: `他对危言耸听的预测进行了修正` },
          { id: 239, topicCn: "", answerFr: `Elles bénéficient d'un effet de mode`, answerCn: `它们受益于流行趋势` },
          { id: 240, topicCn: "", answerFr: `Il se sentait trop vieux pour les tournées`, answerCn: `他觉得自己太老不适合巡演` },
       
        ];

"""

# ---- Config ----
TACHE = 3             # change to 2/3 if you want
KIND = "a"               # "a" for answers; if you insist, change to "q"
OUT_CSV = Path("assets/tcfcaCE/t3.csv")
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
