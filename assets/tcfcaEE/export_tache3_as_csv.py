#!/usr/bin/env python3
import csv
import re
from pathlib import Path

# Paste your JS-style array BELOW, exactly as-is (keys unquoted like id:, topicCn:, answerFr:, etc.)
RAW_JS = r"""
 [
          {
            id: 1, topicCn: "第一段总结",
            answerFr: `Dans le débat sur la question de savoir si ... est/ sont ... ou ..., 
            deux points de vue différents sont présentés par le texte ci-dessus. 
            D’une part, le document 1 soutient/ affirme que + ...; 
            d’autre part, le document 2 estime/ montre que + ...`,
            answerCn: `在关于“[定冠词+名词] 是 [形容词1] 还是[形容词2]”这一问题的讨论中，
            上述文本呈现了两种不同的观点。
            一方面，文件1支持/认为：[完整句子]；
            另一方面，文件2则认为/表明：[完整句子]`
          },
          {
            id: 2, topicCn: "第二段",
            promptFr: "",
            promptCn: "表达观点中立",
            answerFr: `Il me semble que les deux textes présentent des arguments recevables, chacun selon une perspective différente.`,
            answerCn: `我认为这两篇文章都提出了有根据的观点，各自从不同的角度。`
          },
          {
            id: 3, topicCn: "第二段",
            promptFr: "",
            promptCn: "分析两方观点的好处坏处",
            answerFr: `D’un côté, ... apporte/apportent des avantages à + ..., parce que/ comme + ...; 
            de l’autre côté, il/ils/elle/elles peut/peuvent aussi causer/entraîner/provoquer/générer des désagréments à + ...,  parce que/ car/ notamment  + ...`,
            answerCn: `一方面，[名词] 给 [第一批人] 带来好处，因为/由于 [好处(若干)]；
            另一方面，。。。也可能给 [第二批人] 带来不便/麻烦，因为/尤其是因为 [坏处]。`
          },
          {
            id: 4, topicCn: "第二段",
            promptFr: "替换词",
            promptCn: "[第一批人]：",
            answerFr: `à certaines personnes, 
            aux élèves, 
            aux éducateurs et aux parents, 
            aux gens qui n’ont pas beaucoup de temps libre, 
            aux gens qui ont besoin de l’exercice, 
            aux gens`,
            answerCn: `à certaines personnes：对某些人 / 给某些人
aux élèves：对学生 / 给学生
aux éducateurs et aux parents：对教育工作者和家长 / 给教育者和父母
aux gens qui n’ont pas beaucoup de temps libre：对空闲时间不多的人 / 给没有太多空闲时间的人
aux gens qui ont besoin de l’exercice：对需要运动的人 / 给需要锻炼的人
aux gens：对人们 / 给人们`
          },
          {
            id: 5, topicCn: "第二段",
            promptFr: "替换词",
            promptCn: "好处/坏处",
            answerFr: `le gain de temps
le confort de vie
la commodité de la vie
l’économie d’argent/ la réduction des dépenses
l’amélioration de la santé
la réduction du stress mental
l’application dans plusieurs domaines
la diffusion de la culture
l’éducation du grand public

la santé physique
le perte du temps
la mauvaise humeur
la pollution
le bruit
la pression mentale
la détérioration de la santé
la fuite d’informations personnelles
la diminution de la sécurité individuelle
le développement durable des musées`,
            answerCn: `le gain de temps: 节省时间
le confort de vie: 生活的舒适
la commodité de la vie: 生活的便利性
l’économie d’argent/ la réduction des dépenses: 资金的节省
l’amélioration de la santé: 健康状况的提升
la réduction du stress mental: 心理压力的降低
l’application dans plusieurs domaines: 在多个领域中的应用
la diffusion de la culture: 文化的传播
l’éducation du grand public: 大众的教育

la santé physique: 身体健康
le perte du temps: 浪费时间
la mauvaise humeur: 坏的心情
la pollution: 污染
le bruit: 噪音
la pression mentale: 心理压力
la détérioration de la santé: 身体健康的倒退
la fuite d’informations personnelles: 个人信息泄露
la diminution de la sécurité individuelle: 个人安全的下降
le développement durable des musées: 博物馆的可持续发展
`
          },
          {
            id: 6, topicCn: "第二段",
            promptFr: "总结",
            promptCn: "",
            answerFr: `Dans la pratique, il est crucial d’adopter une approche équilibrée en intégrant les points forts dans les deux documents cités tout en anticipant les risques potentiels liés à chacune des positions. 
            Cette synthèse permettra de résoudre les problèmes de manière plus efficace et durable.`,
            answerCn: `在实际操作中，关键在于采取一种平衡的方法，既要整合上述两份文件中的优点，同时也要预先考虑各自立场可能带来的潜在风险。
            通过这种综合性的方式，可以更有效、更持久地解决问题。`
          },

        ];
"""

# ---- Config ----
TACHE = 3                 # set 1/2/3/etc.
KIND  = "a"               # "a" for answers
OUT_CSV = Path("assets/tcfEE/t3.csv")
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
