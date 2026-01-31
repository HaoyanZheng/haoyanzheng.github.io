#!/usr/bin/env python3
import csv
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 [

            {
              id: 1,
              topicCn: "旅游业发展",
              promptFr: "Pour quelles raisons voudrait-on développer le tourisme dans un pays ?",
              promptCn: "为什么一个国家想发展旅游业？",
              answerFr: `Pour quelles raisons voudrait-on développer le tourisme dans un pays ?
Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve très intéressant.
C’est une question assez délicate, car le tourisme peut apporter de nombreux avantages à un pays, mais aussi entraîner certains problèmes s’il est mal encadré. À mon avis, un pays a de bonnes raisons de développer le tourisme, à condition de mettre en place des règles claires et une planification durable.
Tout d’abord, le tourisme permet à un pays d’améliorer son image et son influence à l’international. En accueillant des visiteurs étrangers, un pays peut faire connaître son histoire, ses traditions et ses valeurs. Cela contribue à renforcer sa visibilité et son attractivité sur la scène mondiale. Par exemple, les sites historiques, les musées nationaux et les grands événements culturels permettent de présenter une image positive et ouverte du pays. Ainsi, le tourisme devient un outil de rayonnement culturel et de diplomatie douce.
Ensuite, le tourisme représente un moteur économique important au niveau national. Il crée de nombreux emplois dans des secteurs variés, tels que l’hôtellerie, la restauration, les transports, le commerce et les services. Ces emplois sont accessibles à des profils très différents et peuvent bénéficier à une large partie de la population. De plus, le tourisme génère des revenus pour l’État grâce aux taxes et aux dépenses des visiteurs. Ces ressources peuvent ensuite être utilisées pour soutenir l’économie nationale et améliorer la qualité de vie des citoyens.
Par ailleurs, le tourisme peut jouer un rôle clé dans l’aménagement du territoire. Dans de nombreux pays, les activités économiques sont concentrées dans les grandes villes, ce qui crée des déséquilibres régionaux. Le développement du tourisme permet de valoriser des régions moins connues, comme les zones rurales ou éloignées. Pour accueillir les visiteurs, les autorités sont encouragées à améliorer les infrastructures locales, par exemple les routes, les transports publics et les services de base. Ces améliorations profitent non seulement aux touristes, mais aussi aux habitants, et contribuent à un développement plus équilibré du pays.
Cependant, le tourisme comporte aussi des risques. Une fréquentation excessive peut provoquer des problèmes environnementaux, une surcharge des services publics et une augmentation du coût de la vie pour les résidents. Dans certains cas, le surtourisme peut nuire à la qualité de vie locale. C’est pourquoi il est essentiel de mettre en place des mesures adaptées, comme des limites de fréquentation, des taxes touristiques réinvesties localement et des politiques de protection de l’environnement.
En conclusion, le développement du tourisme permet à un pays de renforcer son image internationale, de stimuler son économie et de favoriser un aménagement plus équilibré du territoire. Toutefois, ce développement doit être encadré par une stratégie durable, afin que les bénéfices profitent à la fois aux habitants et aux visiteurs.
Merci de votre attention.`,
              answerCn: `为了什么原因，一个国家会希望发展旅游业？
谢谢女士、先生给我发言的机会，来讨论这个我觉得很有意思的话题。
这是一个比较微妙的问题，因为旅游业可以为一个国家带来很多好处，但如果缺乏良好的监管，也可能引发一些问题。在我看来，一个国家有充分理由发展旅游业，但前提是要制定清晰的规则并进行可持续的规划。
首先，旅游业可以帮助一个国家提升国际形象与影响力。通过接待外国游客，一个国家能够让更多人了解它的历史、传统和价值观，从而增强其在国际舞台上的能见度与吸引力。例如，历史遗址、国家博物馆和大型文化活动既能吸引游客，也能展示国家积极、开放的形象。因此，旅游业成为文化传播与“软外交”的一种工具。
其次，旅游业在国家层面也是重要的经济动力。它能在酒店、餐饮、交通、商业和服务等多个行业创造大量就业机会。这些岗位面向不同背景的人群，能够惠及更大范围的居民。此外，游客的消费和相关税收也能为国家带来收入，这些资源随后可以用于支持国家经济并改善民众的生活质量。
另外，旅游业还可以在国土与区域发展规划中发挥关键作用。在许多国家，经济活动集中在大城市，导致地区发展不平衡。发展旅游业可以带动一些不太知名的地区，比如农村或偏远地区。为了接待游客，政府会被推动改善当地基础设施，例如道路、公共交通和基本公共服务。这些改善不仅对游客有利，也会让当地居民受益，从而促进更均衡的发展。
不过，旅游业也存在风险。游客过多可能带来环境问题、公共服务超负荷，以及当地生活成本上升，影响居民。在某些情况下，过度旅游还会降低当地生活质量。因此，必须采取适当措施，例如限制游客数量、将旅游税回投本地，以及实施环境保护政策。
总之，发展旅游业可以帮助国家提升国际形象、推动经济增长，并促进更均衡的区域发展。但这一发展必须在可持续战略的框架下进行，才能让居民与游客都从中受益。
谢谢大家的聆听。`
            },

            {
              id: 2,
              topicCn: "互联网利弊，必备手机+游戏，线上工作（相关：远程医疗）",
              promptFr: "Internet apporte-t-il plus d’avantages que d’inconvénients ?",
              promptCn: "互联网带来的好处更多还是坏处更多？",
              answerFr: `Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve intéressant.
C’est une question assez délicate, car Internet a profondément transformé notre vie, que nous le voulions ou non. Il a changé notre manière de communiquer, de travailler et de nous divertir. Selon la façon dont il est utilisé, certains estiment qu’il apporte plus d’avantages, tandis que d’autres pensent qu’il fait plus de mal. Pour ma part, je crois fermement qu’avec une bonne réglementation et un certain contrôle personnel, Internet peut améliorer notre qualité de vie.
D’un côté, il est essentiel de souligner que Internet présente de nombreux aspects positifs. Tout d’abord, c’est un outil de divertissement très important. On peut y regarder la télévision, des films, des émissions, jouer à des jeux et écouter de la musique. Il est devenu une partie indispensable de la vie quotidienne de beaucoup de personnes. Par exemple, une enquête montre que près de 90 % (percent) des gens utilisent Internet chaque jour, notamment pour se détendre après le travail ou les études.
Deuxièmement, Internet facilite la rencontre de nouvelles personnes. Aujourd’hui, il existe de nombreux groupes sur des applications comme WhatsApp qui permettent de rencontrer des personnes partageant les mêmes centres d’intérêt. Par exemple, le week-end, des gens se donnent rendez-vous pour jouer au tennis de table après s’être rencontrés en ligne. Grâce à Internet, ils peuvent aussi échanger avec des passionnés venant de différentes régions.
Cependant, Internet présente également certains inconvénients. Tout d’abord, on peut y trouver des contenus illégaux ou inappropriés, qui peuvent nuire à la santé mentale et physique, comme la désinformation ou certaines formes de propagande. C’est pourquoi il est important que les gouvernements et les entreprises mettent en place des règles claires, comme le contrôle de l’âge, les modes pour mineurs et la modération des contenus.
De plus, une utilisation excessive d’Internet peut entraîner une dépendance. Les réseaux sociaux et les vidéos courtes, par exemple, peuvent devenir très addictifs. Certaines personnes passent plusieurs heures par jour sur leur téléphone, ce qui nuit à leur santé, notamment à la vue et à l’activité physique. Il est donc important de trouver un bon équilibre entre le temps passé en ligne et les activités en plein air.
Enfin, Internet est aussi un espace où existent de nombreuses arnaques. Des personnes mal intentionnées utilisent les plateformes de commerce en ligne, les réseaux sociaux ou les services bancaires pour voler de l’argent. Il est donc essentiel de rester vigilant et de limiter les échanges avec des inconnus en ligne.
En conclusion, même si les avis sont partagés, je pense qu'Internet peut réellement améliorer notre vie, à condition de l’utiliser avec responsabilité, prudence et modération. Merci de votre attention.`,
              answerCn: `谢谢您，女士/先生，给我发言的机会来讨论这个我觉得有趣的话题。

这是一个比较微妙的问题，因为互联网无论我们愿不愿意，都深刻改变了我们的生活：沟通方式、工作方式和娱乐方式都不同了。有人认为它利大于弊，也有人觉得弊大于利。我个人认为，只要有良好的监管和一定的自我控制，互联网确实能提升生活质量。
一方面，互联网有很多积极面：首先，它是重要的娱乐工具，我们可以看电视、电影、节目、玩游戏、听音乐，很多人每天都会使用互联网来放松。
其次，互联网让结识新朋友更容易。比如在 WhatsApp 等应用上有很多兴趣群，人们可以线上认识、线下相约活动，例如周末约打乒乓球，也能与不同地区的同好交流。
但另一方面，互联网也有缺点：首先，存在违法或不适当内容，如虚假信息、宣传操控等，可能伤害身心健康，因此政府和企业需要明确规则，例如年龄验证、青少年模式和内容审核。
其次，过度使用会导致依赖，短视频和社交媒体尤其容易上瘾，很多人每天花数小时刷手机，影响视力与运动量，因此要平衡线上时间与户外活动。
最后，网络诈骗也很多，不法分子利用电商平台、社交网络或网银骗钱，所以必须保持警惕，尽量减少与陌生人的金钱或敏感信息往来。
总之，虽然看法不一，但我认为互联网在负责任、谨慎且适度使用的前提下，确实能改善我们的生活。谢谢您的聆听。`
            },

            {
              id: 3,
              topicCn: "在国外生活是否有利于职业成功",
              promptFr: "Vivre à l’étranger est-il un avantage pour réussir sa carrière professionnelle ?",
              promptCn: "在国外生活是否有利于职业成功？",
              answerFr: `Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve très intéressant.
C’est une question assez délicate, car elle pose le problème de savoir si l’environnement international joue un rôle plus important que les efforts personnels dans la réussite professionnelle. À mon avis, vivre à l’étranger ne garantit pas le succès d’une carrière, mais cela peut constituer un réel avantage dans certains parcours professionnels.
Tout d’abord, vivre à l’étranger permet de développer une meilleure compréhension du monde du travail international. Dans un autre pays, les méthodes de management, l’organisation du travail et la communication professionnelle peuvent être très différentes. Cette expérience aide à mieux comprendre comment fonctionnent les entreprises dans d’autres contextes（浊化） et à s’adapter à des environnements variés. Par exemple, une personne ayant travaillé à l’étranger peut plus facilement collaborer avec des équipes internationales ou s’intégrer dans une entreprise multinationale.
Ensuite, l’expérience à l’étranger renforce fortement les compétences en communication. Travailler ou vivre dans un autre pays oblige souvent à utiliser une langue étrangère et à communiquer avec des personnes issues de cultures différentes. Cela permet d’apprendre à s’exprimer plus clairement, à écouter les autres et à éviter les malentendus. Ces compétences sont très appréciées par les employeurs, notamment dans les secteurs liés au commerce international, à la technologie ou aux services.
De plus, vivre à l’étranger montre une capacité d’adaptation et d’autonomie, des qualités importantes pour réussir professionnellement. S’installer dans un nouveau pays demande de faire face à des situations inconnues, de résoudre des problèmes et de sortir de sa zone de confort. Cette expérience peut renforcer la confiance en soi et la capacité à gérer le stress, ce qui est un avantage dans de nombreux emplois à responsabilités.
Cependant, vivre à l’étranger n’est pas une condition indispensable pour réussir sa carrière. Si une personne souhaite travailler toute sa vie dans son pays d’origine, il peut être plus utile de bien connaître le marché local, les réseaux professionnels et les possibilités de promotion. Dans ce cas, l’expérience locale et les résultats concrets peuvent （浊化）avoir plus de valeur que l’expérience internationale.
En conclusion, vivre à l’étranger peut représenter un avantage important pour réussir sa carrière professionnelle, surtout dans un contexte international. Toutefois, ce n’est pas une garantie de succès : la motivation personnelle, les compétences et le travail restent essentiels.
Merci de votre attention.`,
              answerCn: `谢谢女士、先生给我发言的机会，来讨论这个我觉得很有意思的话题。
这是一个比较微妙的问题，因为它涉及：在职业成功中，国际化环境是否比个人努力更重要。在我看来，在国外生活并不能保证职业成功，但在某些职业路径中，它确实可能成为一个真实的优势。
首先，在国外生活能让人更好地理解国际化的职场环境。在另一个国家，管理方式、工作组织以及职场沟通可能都非常不同。这段经历能帮助人更好理解不同背景下企业如何运作，并学会适应多样的工作环境。例如，有海外工作经验的人，往往更容易与国际团队合作，或融入跨国公司。
其次，海外经历能显著提升沟通能力。在国外工作或生活通常需要使用外语，并与来自不同文化的人交流。这会让人学会更清晰地表达、更好地倾听，并减少误解。这类能力很受雇主欢迎，尤其是在国际贸易、科技或服务等行业。
此外，在国外生活还能体现一个人的适应能力和独立性，而这些都是职业成功的重要素质。搬到一个新国家意味着要面对陌生情况、解决问题、走出舒适区。这种经历能增强自信，提高抗压能力，在许多需要承担责任的岗位上都是加分项。
不过，在国外生活并不是职业成功的必要条件。如果一个人计划一生都在本国发展，那么更了解本地市场、职业人脉以及晋升机会，可能更有用。在这种情况下，本地经验和可量化的成果，可能比国际经历更有价值。
总之，在国外生活在国际化背景下确实可能为职业发展带来重要优势，但它并不能保证成功：个人动机、能力以及持续努力仍然是关键。谢谢大家的聆听。`
            },

            {
              id: 4,
              topicCn: "父母权威是否必要",
              promptFr: "Est-ce que l’autorité est nécessaire dans l’éducation d’un enfant ?",
              promptCn: "在教育孩子时，权威是否有必要？",
              answerFr: `Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve très intéressant.
C’est une question assez délicate, car elle oppose deux idées importantes : d’un côté, la liberté de l’enfant, et de l’autre, l’autorité des parents. Faut-il laisser l’enfant faire ses propres choix, ou bien lui imposer certaines règles ? À mon avis, l’autorité est nécessaire dans l’éducation d’un enfant, mais elle doit être raisonnable, bienveillante et surtout adaptée à l’âge de l’enfant.
Tout d’abord, l’autorité est indispensable pour assurer la sécurité et le bien-être de l’enfant. Les parents ont plus d’expérience de la vie et sont mieux placés pour évaluer les dangers. Les enfants, en revanche, ne mesurent pas toujours les conséquences de leurs actes. Par exemple, un enfant peut traverser la rue sans regarder, manger de manière déséquilibrée ou faire confiance à des inconnus. Dans ces situations, l’autorité parentale permet de fixer des limites claires et de protéger l’enfant.
Ensuite, l’autorité joue un rôle essentiel dans l’apprentissage des règles et du respect, y compris dans le monde numérique. Dès le plus jeune âge, les enfants doivent comprendre qu’il existe des règles à la maison, à l’école et dans la société. Apprendre à respecter les horaires, les consignes des enseignants ou les règles de politesse aide l’enfant à mieux vivre avec les autres. Aujourd’hui, cela concerne aussi l’usage d’Internet et des écrans. Sans cadre, les enfants peuvent passer trop de temps en ligne ou être exposés à des contenus inadaptés. L’autorité permet donc d’encadrer ces usages et de préparer l’enfant à devenir un citoyen responsable.
Par ailleurs, l’autorité doit évoluer en fonction de l’âge de l’enfant. Un jeune enfant a besoin de règles simples et claires, tandis qu’un adolescent a davantage besoin 2d’accompagnement et de confiance. L’objectif de l’autorité n’est pas de contrôler l’enfant en permanence, mais de l’aider progressivement à prendre ses propres décisions. En adaptant l’autorité à l’âge et à la maturité de l’enfant, les parents favorisent le développement de l’autonomie et du sens des responsabilités.
Cependant, l’autorité ne doit jamais être excessive ni autoritaire. Une éducation fondée uniquement sur l’obéissance peut freiner la confiance en soi et empêcher l’enfant de développer son esprit critique. C’est pourquoi l’autorité doit toujours s’accompagner de dialogue et d’explications. Lorsque l’enfant comprend le sens des règles, il les accepte plus facilement et apprend à réfléchir par lui-même.
En conclusion, je pense que l’autorité est indispensable dans l’éducation d’un enfant, mais qu’elle doit rester équilibrée et adaptée à son âge. Une autorité bienveillante, basée sur le respect et le dialogue, permet à l’enfant de grandir en sécurité, de développer son autonomie et de devenir un adulte responsable.
Merci de votre attention.`,
              answerCn: `谢谢女士、先生给我发言的机会，来讨论这个我觉得很有意思的话题。
这是一个比较微妙的问题，因为它对立了两个重要观念：一方面是孩子的自由，另一方面是父母的权威。到底应该让孩子自己做选择，还是必须给他设定一些规则？在我看来，教育孩子需要权威，但这种权威必须合理、善意，并且最重要的是要符合孩子的年龄。
首先，权威对于保障孩子的安全与身心健康是不可或缺的。父母拥有更多生活经验，更能评估危险；而孩子往往无法意识到自己行为的后果。比如，孩子可能过马路不看路、饮食不均衡，或轻易相信陌生人。在这些情况下，父母的权威能设定清晰的界限，从而保护孩子。
其次，权威在学习规则与尊重方面起着关键作用，包括在数字世界里也是如此。从很小的时候开始，孩子就需要明白：在家里、在学校以及在社会中都存在必须遵守的规则。学会遵守时间、遵守老师的要求、遵守礼貌规范，能帮助孩子更好地与他人相处。如今，这也涉及互联网和屏幕的使用。如果没有约束，孩子可能上网时间过长，或接触到不适合的内容。因此，父母的权威可以用来规范这些使用方式，并帮助孩子成长为负责任的公民。
此外，权威应当随着孩子年龄的增长而变化。年纪小的孩子需要简单明确的规则；而青少年更需要陪伴与信任。权威的目标不是时刻控制孩子，而是逐步帮助他学会自己做决定。父母根据孩子的年龄和成熟度调整权威方式，能促进孩子形成自主能力和责任感。
不过，权威绝不能过度，也不能变成专制。只强调服从的教育方式，可能会阻碍孩子自信心的发展，并让他难以形成批判性思维。因此，权威必须始终伴随对话与解释。当孩子理解规则的意义时，他更容易接受，也会学会独立思考。
总之，我认为权威在教育孩子时是不可或缺的，但必须保持平衡，并与孩子的年龄相匹配。以尊重和对话为基础的善意权威，能让孩子在安全中成长，发展自主能力，并成为一个负责任的成年人。谢谢大家的聆听。`
            },

            {
              id: 5,
              topicCn: "公共交通是否应免费以保护环境",
              promptFr: "Pour protéger la planète, les transports publics devraient-ils être gratuits ?",
              promptCn: "为了保护地球，公共交通是否应该免费？",
              answerFr: `Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve très intéressant.
C’est une question assez délicate, car rendre les transports publics gratuits peut avoir des effets positifs sur l’environnement, mais aussi poser certains défis pratiques. À mon avis, la gratuité des transports publics peut contribuer à protéger la planète, mais elle doit être mise en place de manière ciblée et progressive, et non de façon totale et immédiate.
D’un côté, rendre les transports publics gratuits est un moyen efficace d’encourager les citoyens à réduire l’usage de la voiture individuelle. Lorsque les bus, métros ou tramways sont gratuits, de nombreuses personnes sont incitées à laisser leur voiture à la maison. Cela permet de diminuer le nombre de véhicules sur les routes, de réduire les embouteillages et de limiter les émissions de gaz à effet de serre. De plus, moins de voitures signifie aussi moins d’accidents de la route et moins de pollution sonore, ce qui améliore la qualité de vie en ville.
Ensuite, la gratuité des transports publics peut favoriser des comportements plus écologiques, surtout dans les grandes villes. Les déplacements domicile-travail représentent une part importante de la pollution quotidienne. Rendre les transports gratuits pendant les heures de pointe, par exemple le matin et le soir, pourrait réduire fortement l’impact environnemental lié aux trajets professionnels. Cette mesure encouragerait un changement durable des habitudes de déplacement, ce qui est essentiel pour protéger la planète à long terme.
Cependant, rendre les transports publics entièrement gratuits pose aussi des limites. Dans certaines régions rurales ou peu desservies, les transports publics ne sont pas suffisamment développés pour remplacer la voiture. De plus, dans les grandes villes, une gratuité totale pourrait entraîner une surcharge du réseau, avec des bus et des métros trop remplis, ce qui nuirait à la qualité du service. Il faut également tenir compte du coût financier pour les gouvernements, car l’entretien et le développement des infrastructures restent indispensables.
C’est pourquoi une solution intermédiaire semble plus réaliste. Par exemple, la gratuité pourrait être réservée à certains groupes, comme les jeunes, les personnes âgées ou les ménages à faible revenu. Elle pourrait aussi s’appliquer uniquement à certaines périodes ou dans certaines zones urbaines. En parallèle, les gouvernements doivent continuer à investir dans des transports publics plus efficaces, propres et bien connectés.
En conclusion, rendre les transports publics gratuits peut aider à protéger la planète, mais seulement si cette mesure est bien adaptée au contexte local. Une politique ciblée, combinée à des investissements durables, permettrait de réduire la pollution tout en garantissant un service de qualité pour les citoyens.
Merci de votre attention.`,
              answerCn: `谢谢女士、先生给我发言的机会，来讨论这个我觉得很有意思的话题。
这是一个比较微妙的问题，因为让公共交通免费可能对环境产生积极影响，但也会带来一些实际挑战。在我看来，公共交通免费确实有助于保护地球，但应当以有针对性、循序渐进的方式推行，而不是立刻全面免费。
一方面，让公共交通免费是一种有效方式，可以鼓励市民减少使用私人汽车。当公交车、地铁或有轨电车免费时，很多人会更愿意把车留在家里。这能减少道路上的车辆数量，缓解拥堵，并降低温室气体排放。此外，车更少也意味着交通事故更少、噪音污染更低，从而提升城市生活质量。
其次，公共交通免费还能促进更环保的出行行为，尤其是在大城市。通勤出行（上下班）是日常污染的重要来源之一。比如，如果在早晚高峰时段提供免费乘车，就可能显著降低与工作通勤相关的环境影响。这种措施也能推动人们形成更长期、更稳定的出行习惯改变，而这对长期保护地球很关键。
不过，全面免费也有其局限。在一些农村或公共交通覆盖较少的地区，公共交通本身并不完善，难以替代私家车。此外，在大城市，如果完全免费，可能导致网络超负荷，出现公交和地铁过度拥挤，从而影响服务质量。还要考虑政府的财政负担，因为公共交通的维护与扩建仍然必不可少。
因此，一个折中的方案更现实。例如，免费政策可以优先面向某些群体，比如青少年、老年人或低收入家庭；也可以只在特定时段或特定城市区域实行。同时，政府还应持续投资建设更高效、更清洁、衔接更好的公共交通系统。
总之，公共交通免费确实可能帮助保护地球，但前提是政策要符合当地实际。采取有针对性的免费政策，并与可持续投资相结合，既能减少污染，也能保障市民获得高质量的公共交通服务。谢谢大家的聆听。`
            },

            {
              id: 6,
              topicCn: "单身是否能幸福",
              promptFr: "Peut-on vivre heureux en étant célibataire ?",
              promptCn: "单身可以过得幸福吗？",
              answerFr: `Peut-on vivre heureux en étant célibataire ?
Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve très intéressant.
C’est une question assez délicate, car dans de nombreuses sociétés, le bonheur est souvent associé au couple, au mariage et à la famille. Pourtant, à mon avis, il est tout à fait possible de vivre heureux en étant célibataire. Le bonheur ne dépend pas uniquement du statut marital, mais plutôt de l’équilibre personnel, des choix de vie et de la qualité des relations, qu’elles soient amoureuses ou non.
Tout d’abord, être célibataire offre une grande liberté dans l’organisation de la vie quotidienne. Une personne célibataire peut prendre ses décisions seule, gérer son temps libre comme elle le souhaite et poursuivre ses propres projets sans compromis constants. Par exemple, dans les grandes villes, il est facile de participer à des activités culturelles, à des événements sociaux ou sportifs, et de profiter de la vie urbaine de manière autonome. Cette liberté peut être une source importante de satisfaction personnelle.
Ensuite, le célibat permet de se concentrer davantage sur le développement personnel. Être célibataire donne l’occasion de mieux se connaître, de développer ses passions et de renforcer son indépendance émotionnelle. Certaines personnes utilisent cette période pour voyager, reprendre des études, progresser dans leur carrière ou s’investir dans des activités créatives. Ces expériences peuvent apporter un sentiment d’accomplissement et de bonheur durable, sans nécessairement passer par une relation amoureuse.
De plus, le bonheur ne dépend pas uniquement du fait d’être en couple, mais de la qualité des relations que l’on entretient. Une relation amoureuse négative ou conflictuelle peut au contraire réduire la qualité de vie et provoquer du stress ou de l’insatisfaction. Être célibataire permet d’éviter des relations malsaines et de privilégier des liens sociaux positifs, comme l’amitié, la famille ou la vie associative. Ces relations peuvent être tout aussi importantes pour le bien-être émotionnel.
Cependant, il est vrai que le célibat peut aussi présenter des défis, comme le sentiment de solitude, surtout dans certaines périodes de la vie. C’est pourquoi il est essentiel pour une personne célibataire de maintenir une vie sociale active et de construire un réseau de soutien solide. Le bonheur en célibat demande donc un certain équilibre et une capacité à créer du sens dans sa vie.
En conclusion, je pense qu’on peut tout à fait vivre heureux en étant célibataire. Le bonheur dépend avant tout de la liberté de choisir son mode de vie, de la qualité des relations et de l’épanouissement personnel. Être célibataire n’est pas un échec, mais simplement une autre façon de construire une vie heureuse.
Merci de votre attention.`,
              answerCn: `单身可以过得幸福吗？
谢谢女士、先生给我发言的机会，来讨论这个我觉得很有意思的话题。
这是一个比较微妙的问题，因为在很多社会里，人们常常把幸福与恋爱、婚姻和家庭联系在一起。然而在我看来，一个人完全可以在单身状态下过得幸福。幸福并不只取决于婚恋状态，而更取决于个人的平衡、生活选择，以及各种关系的质量——不论是爱情关系还是非爱情关系。
首先，单身能带来更大的生活自由。在日常生活的安排上，单身人士可以独立做决定，按自己的意愿管理时间，也能更专注于自己的计划，而不需要不断妥协。例如，在大城市里，人们很容易参加文化活动、社交或体育活动，并以更独立的方式享受城市生活。这种自由本身就可能成为重要的满足感来源。
其次，单身也让人更能专注于自我成长。单身提供了一个更了解自己的机会，可以发展兴趣爱好，并增强情感上的独立性。有些人会利用这段时间去旅行、继续学习、提升职业发展，或投入到创造性活动中。这些经历能够带来成就感与更长期的幸福感，而并不一定要通过恋爱关系来实现。
此外，幸福并不只取决于是否有伴侣，更取决于关系质量。相反，一段负面或充满冲突的恋爱关系，可能降低生活质量，带来压力与不满。单身可以让人避免不健康的关系，并把精力投入到更积极的社会关系中，比如友情、家庭关系或志愿/社团生活。这些关系同样能够为情感健康提供重要支持。
不过，单身也确实可能带来一些挑战，比如在某些人生阶段更容易感到孤独。因此，单身人士需要保持积极的社交生活，并建立可靠的支持网络。也就是说，单身的幸福需要一定的平衡能力，以及为生活创造意义的能力。
总之，我认为单身完全可以过得幸福。幸福主要来自能够自由选择生活方式、维持高质量的人际关系，以及实现个人成长。单身不是失败，而只是另一种建立幸福人生的方式。谢谢大家的聆听。`
            },

            {
              id: 7,
              topicCn: "年轻人排斥变老",
              promptFr: "De nos jours, les jeunes rejettent l'idée de vieillir. Quel est votre avis sur cette idée?",
              promptCn: "如今，年轻人排斥变老这一想法。你怎么看？",
              answerFr: `Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve très intéressant.
C’est une question assez délicate, car elle touche aux valeurs de la société moderne et à la manière dont les jeunes perçoivent le temps et l’avenir. À mon avis, il est vrai qu’aujourd’hui, de nombreux jeunes semblent rejeter l’idée de vieillir, mais ce phénomène s’explique par des changements sociaux et culturels, et il présente à la fois des aspects positifs et négatifs.
D’un côté, les modes de vie actuels ont profondément modifié le lien entre l’âge et le style de vie. Dans les sociétés modernes, certaines activités autrefois associées à la jeunesse, comme voyager, se divertir ou apprendre de nouvelles compétences, sont aujourd’hui accessibles à tous les âges. Grâce aux progrès technologiques et à l’amélioration des conditions de vie, les jeunes peuvent avoir l’impression que vieillir n’entraîne plus de changements importants dans la vie quotidienne. Ainsi, l’âge est perçu davantage comme un chiffre que comme une véritable limite.
De plus, les avancées dans le domaine de la santé et de la nutrition ont augmenté l’espérance de vie et amélioré la qualité de vie des personnes âgées. Les jeunes savent qu’ils peuvent rester en bonne santé plus longtemps et continuer à être actifs à un âge avancé. Cela peut expliquer pourquoi ils se sentent moins concernés par le vieillissement et repoussent cette idée à plus tard. Vieillir n’est plus forcément associé à la maladie ou à la dépendance, comme c’était le cas auparavant.
Cependant, rejeter l’idée de vieillir peut aussi être une forme de refus de la réalité. Le vieillissement est un processus naturel qui concerne tout le monde, et l’ignorer peut entraîner des difficultés plus tard. Par exemple, certains jeunes ne se préparent pas suffisamment à l’avenir, que ce soit sur le plan financier, professionnel ou personnel. En refusant de penser au vieillissement, ils risquent de manquer d’anticipation et de maturité face aux responsabilités de la vie adulte.
Enfin, la société actuelle valorise fortement la jeunesse, l’apparence physique et la performance. Les réseaux sociaux renforcent cette image en mettant en avant des modèles jeunes et idéalisés. Cette pression sociale peut pousser les jeunes à craindre le vieillissement et à le considérer comme quelque chose de négatif, voire comme un échec.
En conclusion, je pense que si les jeunes rejettent l’idée de vieillir, c’est surtout en raison des transformations de la société moderne. Toutefois, accepter le vieillissement comme une étape naturelle de la vie permet de mieux se préparer à l’avenir et de construire un parcours de vie plus équilibré.
Merci de votre attention.`,
              answerCn: `谢谢女士、先生给我发言的机会，来讨论这个我觉得很有意思的话题。
这是一个比较微妙的问题，因为它涉及现代社会的价值观，以及年轻人如何看待时间与未来。在我看来，确实，如今不少年轻人似乎在排斥“变老”这一概念，但这种现象可以用社会与文化的变化来解释，同时也既有积极面，也有消极面。
一方面，当代生活方式深刻改变了“年龄”和“生活方式”之间的关系。在现代社会里，一些过去通常与年轻联系在一起的活动，比如旅行、娱乐或学习新技能，如今在任何年龄段都可以实现。随着科技进步和生活条件改善，年轻人可能觉得变老并不会在日常生活中带来很大变化。因此，年龄更多被看作一个数字，而不是一个真正的限制。
此外，健康与营养领域的进步提高了人们的寿命，也改善了老年人的生活质量。年轻人知道自己可以更长时间保持健康，并在较大年龄仍然保持活跃。这也解释了为什么他们对衰老的感受没那么强烈，甚至把“变老”这件事推到以后再考虑。变老不再必然与疾病或依赖联系在一起，正如过去那样。
然而，排斥变老也可能是一种对现实的拒绝。衰老是一个自然过程，人人都会经历；如果忽视它，将来可能会遇到困难。例如，一些年轻人对未来准备不足，无论是在财务、职业还是个人生活方面。因为不愿思考衰老，他们可能缺乏前瞻性，也更难以成熟地面对成年生活的责任。
最后，当今社会非常推崇年轻、外貌与表现。社交媒体进一步强化了这种形象，持续呈现年轻、理想化的榜样。这种社会压力可能让年轻人害怕变老，把它视为负面的事情，甚至认为是一种失败。
总之，我认为年轻人排斥变老，主要是现代社会变化所带来的结果。不过，把衰老视为人生的自然阶段，更有助于人们为未来做好准备，并建立更平衡的人生道路。
谢谢大家的聆听。`
            },

            {
              id: 8,
              topicCn: "媒体是否应限制暴力画面传播",
              promptFr: "Les médias doivent-ils limiter la diffusion d’images violentes dans les journaux télévisés ? Quels sont les enjeux éthiques et informatifs ?",
              promptCn: "媒体是否应该在电视新闻中限制暴力画面？伦理与信息层面的争议是什么？",
              answerFr: `Merci Madame, Monsieur de m’avoir donné la parole pour discuter de ce sujet que je trouve très intéressant.
C’est une question assez délicate, car les médias ont une double responsabilité : informer le public de manière complète et fidèle, tout en respectant la sensibilité des téléspectateurs. À mon avis, les médias doivent limiter la diffusion d’images violentes dans les journaux télévisés, sans pour autant cacher la réalité des faits. Il s’agit donc de trouver un équilibre entre le devoir d’informer et la responsabilité éthique.
D’un côté, les images violentes peuvent jouer un rôle informatif important. Montrer certaines images permet au public de comprendre la gravité d’un événement, comme une guerre, un attentat ou une catastrophe. Sans images, l’information peut paraître abstraite ou minimisée. Les journalistes ont donc le devoir de montrer la réalité afin d’éviter la désinformation et de permettre aux citoyens de se faire une opinion éclairée. Sur le plan informatif, ces images peuvent renforcer la transparence et la crédibilité des médias.
Cependant, la diffusion d’images violentes pose de sérieux enjeux éthiques. Ces images peuvent provoquer des chocs émotionnels, de l’anxiété ou de la peur, surtout chez les enfants et les personnes vulnérables. Une exposition répétée à la violence peut aussi banaliser la souffrance humaine et nuire à la qualité de vie du public. Les médias ont donc la responsabilité de protéger leur audience et d’éviter une diffusion excessive ou sensationnaliste de la violence.
De plus, la diffusion d’images violentes peut parfois servir involontairement les intérêts des auteurs de violences. Dans le cas du terrorisme ou de certains crimes, la médiatisation excessive peut amplifier la peur et donner une visibilité recherchée par les criminels. Sur le plan éthique, les médias doivent éviter de devenir un outil de manipulation émotionnelle ou de propagande, même indirectement.
C’est pourquoi une limitation encadrée semble nécessaire. Par exemple, les médias peuvent flouter certaines images, avertir le public avant leur diffusion ou privilégier des descriptions verbales plutôt que des images choquantes. Cette approche permet d’informer sans traumatiser, tout en respectant les principes éthiques du journalisme.
En conclusion, les médias doivent limiter la diffusion d’images violentes dans les journaux télévisés, non pas pour censurer l’information, mais pour la diffuser de manière responsable. Trouver un équilibre entre information et éthique est essentiel pour informer le public tout en respectant sa dignité et sa sensibilité.
Merci de votre attention.`,
              answerCn: `谢谢女士、先生给我发言的机会，来讨论这个我觉得很有意思的话题。
媒体是否应该在电视新闻中限制暴力画面的传播？这是一个比较棘手的问题，因为媒体有两项责任：一方面要真实、完整地向公众提供信息；另一方面也要保护观众，尤其是更脆弱的人群。在我看来，媒体确实应该限制这类画面，但不能因此掩盖事实。目标是以负责任的方式呈现现实。
一方面，画面具有真实的信息价值。它能帮助公众理解战争、恐怖袭击或灾难事件的严重性。如果没有画面，一些事件可能显得遥远，甚至被淡化。展示画面（哪怕令人不适）可以帮助公民形成自己的判断，理解政治与社会层面的影响，并减少虚假信息的空间。如果信息经过核实并提供背景解释，这也能提升媒体的可信度。
但另一方面，伦理风险很大。过于暴力的画面可能造成心理冲击，引发焦虑，甚至带来创伤，尤其对儿童更明显。反复接触暴力也可能让人对痛苦麻木，产生情绪疲劳。此外，这还涉及“尊严”问题：拍摄受害者、展示尸体或羞辱性的场景，可能对当事人及其家属不尊重。还有一个风险是“哗众取宠”：一些频道为了收视率而利用暴力画面，这与新闻伦理不相容。
另一个重要点是被操控的风险。在某些情况下，特别是恐怖主义事件，传播这些画面可能反而服务了施暴者：扩大恐惧、提供曝光，甚至引发模仿。因此，媒体必须避免在无意中成为宣传或煽动的渠道。
因此，需要一种“有规范的限制”。媒体可以：对最冲击的画面打马赛克、剪掉某些镜头、在播出前给出明确警告、选择不那么直白的画面，或者在画面过于暴力时用语言描述替代。最关键的是提供背景：解释为什么要展示某个画面，以及它对理解事件到底有什么帮助。
总之，限制暴力画面并不等于审查或掩盖现实，而是以负责任的方式报道，在尊重受害者尊严的同时，也照顾公众的心理承受能力。谢谢大家的聆听。`
            }
          ]

"""

# ---- Config ----
TACHE = 1             # change to 2/3 if you want
KIND = "a"               # "a" for answers; if you insist, change to "q"
OUT_CSV = Path("assets/tcfEO/t1.csv")
# ----------------


def extract_answerfr_strings(text: str) -> list[str]:
    """
    Extracts the quoted string after answerFr: "..."
    Assumes answerFr values use double quotes.
    """
    answers = []
    key = 'answerFr: "'
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
                elif ch == '"':
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
