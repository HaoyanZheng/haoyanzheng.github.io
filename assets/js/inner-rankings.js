(() => {
  "use strict";

  const rankings = {
    anime: {
      title: "动画榜", kicker: "ANIME RANKING",
      items: [
        ["安达与岛村",8,7,3,4,"10.0"],["恋人不行 / わたなれ",9,10,9,3,"10.0"],["樱Trick",10,10,10,0,"10.0"],["牵牛花与加濑同学",10,7,9,1,"9.8"],["终将成为你",8.5,5,8,4,"9.6"],["转生王女与天才千金的魔法革命",8,7,7,4,"9.3"],["我爱上了坏女人大小姐",9,10,6,3,"9.2"],["想吃掉我的非人少女",3,2,4,9,"9.0"],["超时空辉夜姬！",7,8,5,4,"8.9"],["恋语轻唱",8,6,7,4,"8.8","⚠️胃"],["与你相恋到生命尽头",5,3,6,9,"8.7"],["时光沙漏 / Fragtime",8,5,8,4,"8.6"],["憧憬成为魔法少女",6,10,9,2,"8.5","🌶️"],["百合熊风暴",4,5,8,8,"8.4"],["里世界郊游",6,5,5,6,"8.4"],["小林家的龙女仆",7,9,4,2,"8.3"],["摇曳百合",7,10,3,0,"8.3"],["家里蹲吸血姬的苦闷",6,8,5,5,"8.1"],["Citrus",5,4,9,7,"7.9","⚠️胃"],["恶魔之谜",5,5,5,6,"7.8"],["和机器人……能算经验次数吗？",6,9,10,1,"7.8","🌶️"],["我的百合乃工作是也！",4,6,5,8,"7.5","⚠️胃"],["水星的魔女",5,5,4,7,"7.5"],["神推偶像登上武道馆我就死而无憾",5,9,3,3,"7.4"],["少女革命",3,4,6,9,"7.3"],["魔法少女奈叶",5,6,3,5,"7.1"],["NEW GAME!",5,9,2,1,"7.0"],["请问今天要来点兔子吗？",5,9,2,0,"6.9"],["天才麻将少女",5,7,2,3,"6.8"],["魔法少女小圆",2,2,3,10,"6.6"],["少女派别 / Shōjo Sect",5,4,10,4,"成人OVA，单列","🔞"],["花吻在上 OVA",9,6,10,0,"成人OVA，单列","🔞"]
      ]
    },
    manga: {
      title: "漫画榜", kicker: "MANGA RANKING",
      items: [
        ["樱Trick",10,10,10,0,"10.0"],["牵牛花与加濑同学",10,7,9,1,"9.9"],["放课后",9.5,8,10,1,"9.8"],["愉快的失忆 / Cheerful Amnesia",10,10,9,1,"9.8"],["终将成为你",8.5,5,8,4,"9.7"],["无法拒绝孤独的她",10,8,9,2,"9.7"],["温热的银莲花",10,7,8,2,"9.6"],["老师也在谈恋爱！",10,8,9,1,"9.6"],["Girl Friends",9,8,8,3,"9.5"],["志乃与恋",10,8,8,1,"9.5"],["飞野同学是笨蛋",9,10,8,1,"9.4"],["Hana & Hina After School",9,8,8,2,"9.4"],["在意的人不是异性",9,8,6,2,"9.3"],["即使只有一次也会后悔",9,7,8,2,"9.2"],["绝对想当姐姐的义姐 VS 绝对想搞百合的义妹",9,10,7,1,"9.1"],["你我的双人间",9,8,5,1,"9.0"],["一周一次买下同班同学的那些事 漫画版",8,5,8,3,"9.0"],["恋语轻唱",8,6,7,4,"8.8","⚠️胃"],["感染她嘴唇的欲望",8,7,8,2,"8.7"],["初恋构造式",8,7,6,3,"8.6"],["譜为君嗥",8,7,6,3,"8.5"],["恋爱女子课",8,7,7,3,"8.5"],["百合要从奴隶开始",7,8,7,4,"8.3"],["霓裳于舞室起舞",7,5,6,4,"8.2"],["吸血鬼学姐×学妹",7,5,7,5,"8.1"],["月不会数羊",7,6,6,4,"8.0"],["妾愿为君亡",6,9,5,2,"7.9"],["夕辉海石 / 夕凪マーブレット",7,6,6,4,"7.8"],["雨中 你那身影所向之处",7,5,6,4,"7.7"],["Citrus",5,4,9,7,"7.6","⚠️胃"],["彩纯对蕾丝风俗大感兴趣",7,8,10,2,"7.6","🌶️"],["和机器人……能算经验次数吗？",7,8,10,2,"7.5","🌶️"],["无法向星星许愿的恋情",5,3,6,7,"7.0","⚠️胃"],["无法白“嫖”",5,7,9,6,"6.9","🌶️"],["与你相恋到生命尽头",6,3,6,9,"8.3＊"],["我的百合乃工作是也",4,6,5,8,"6.5","⚠️胃"],["今日女友不在",2,2,9,9,"5.0","⚠️胃"],["毁掉一切，地狱再爱",1,2,8,10,"4.8","⚠️胃"],["脏可爱",0,1,10,10,"4.0","⚠️胃"],["与你编缀的泡沫",5,2,6,10,"7.5＊"]
      ]
    },
    novel: {
      title: "轻小说榜", kicker: "LIGHT NOVEL RANKING",
      items: [
        ["安达与岛村",9,7,"5→↑",4,"10.0"],["恋人不行 / わたなれ",9,10,9,3,"9.9"],["一周一次买下同班同学的那些事",9,6,9,3,"9.7"],["性格恶劣的天才青梅",8,7,9,4,"9.2"],["我爱上了坏女人大小姐",8.5,9,7,3,"9.1"],["转生王女与天才千金的魔法革命",8,7,7,4,"9.0"],["班上的公主是我的小狗",8,8,8,3,"8.9"],["里世界郊游",6,5,"5→↑",6,"8.5"],["家里蹲吸血姬的苦闷",6,8,5,5,"8.2"],["我心爱之人的妹妹",6,5,7,7,"7.4","⚠️胃"],["狱门抚子在此",3,4,4,8,"7.2"]
      ]
    }
  };

  const body = document.querySelector("#ranking-body");
  const search = document.querySelector("#ranking-search");
  const empty = document.querySelector("#empty-state");
  const count = document.querySelector("#result-count");
  const title = document.querySelector("#list-title");
  const kicker = document.querySelector("#list-kicker");
  const tabs = [...document.querySelectorAll(".tab")];
  let activeList = "anime";

  const rankLabel = (rank) => rank;
  const numericValue = (value) => Number.parseFloat(String(value)) || 0;
  const valueCell = (value) => `<span class="value${numericValue(value) >= 9 ? " top" : ""}">${value}</span>`;

  function render() {
    const list = rankings[activeList];
    const query = search.value.trim().toLocaleLowerCase("zh-CN");
    const matches = list.items
      .map((item, index) => ({ item, rank: index + 1 }))
      .filter(({ item }) => `${item[0]} ${item[6] || ""}`.toLocaleLowerCase("zh-CN").includes(query));

    title.textContent = list.title;
    kicker.textContent = list.kicker;
    count.textContent = query ? `找到 ${matches.length} 部` : `共 ${list.items.length} 部`;
    empty.hidden = matches.length !== 0;
    body.hidden = matches.length === 0;
    body.innerHTML = matches.map(({ item, rank }) => `
      <tr>
        <td><span class="rank${rank <= 3 ? " podium" : ""}">${rankLabel(rank)}</span></td>
        <td class="work"><strong>${item[0]}</strong>${item[6] ? `<span class="flag" title="内容提示">${item[6]}</span>` : ""}</td>
        <td>${valueCell(item[1])}</td>
        <td>${valueCell(item[2])}</td>
        <td>${valueCell(item[3])}</td>
        <td>${valueCell(item[4])}</td>
        <td><span class="score">${item[5]}</span></td>
      </tr>`).join("");
  }

  tabs.forEach((tab) => tab.addEventListener("click", () => {
    activeList = tab.dataset.list;
    tabs.forEach((item) => {
      const selected = item === tab;
      item.classList.toggle("is-active", selected);
      item.setAttribute("aria-selected", String(selected));
    });
    render();
  }));

  search.addEventListener("input", render);
  render();
})();
