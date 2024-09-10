    var tanm = ["長恨此身非我有 何時忘卻營營 - 蘇軾《臨江仙·夜歸臨皋》",
		"是非成敗轉頭空 青山依舊在 幾度夕陽紅 - 楊慎《臨江仙·滾滾長江東逝水》", 
		"小樓昨夜又東風 故國不堪回首月明中 - 李煜《虞美人·春花秋月何時了》",
		"人生若只如初見 何事秋風悲畫扇 - 納蘭性德《木蘭花·擬古決絶詞柬友》",
		"同是天涯淪落人 相逢何必曾相識 - 白居易《琵琶行》",
		"今年歡笑復明年 秋月春風等閒度 - 白居易《琵琶行》",
		"夜深忽夢少年事 夢啼妝淚紅闌干 - 白居易《琵琶行》",
		"芙蓉如面柳如眉 對此如何不淚垂 - 白居易《琵琶行》"
		];
    (function f(win, doc) {
        var danmArrayTop = []; //15个 同时
        var danmArrayBottom = []; //15个 同时
        var danmMoveDuration = 40;
        var movPx = 2;
        var startPosition = Math.ceil(Math.random() * 100);
        var topContainer = null;
        var bottomContainer = null;
        var createDanmDuration = 0;
        $(document).ready(function () {
            calculateRemPx();
            initPage();
            initDanm();
            initCartoon();
        });
        win.onload = function () {
            let diffWidth = $(document).width() - $(win).width();
            if (diffWidth > 0) {
                setTimeout(function () {
                    win.scrollTo && win.scrollTo(diffWidth / 2, 0);
                }, 0);
            }
        };
        function danm(el, speed, p) {
            this.el = el;
            this.position = p;
            this.speed = speed;
            this.width = -p;
            this.state = "run";
        }
        danm.prototype.delete = function () {
            this.state = "delete";
            $(this.el).remove();
        };
        function initDanm() {
            topContainer = $("#dwn-dm-top");
            bottomContainer = $("#dwn-dm-bottom");
            setInterval(moveDanm, danmMoveDuration);
        }
        function moveDM(b) {
            var docWidth = $(doc).width();
            if (b.position > (docWidth + b.width)) {
                b.delete();
            }
            else if (b.state === 'run') {
                b.position = b.position + b.speed;
                b.el.style.right = b.position + "px";
            }
        }
        function moveDanm() {
            if(createDanmDuration>=20000){
                createDanm();
                createDanmDuration=0;
            }
             createDanmDuration+=danmMoveDuration;
            danmArrayBottom.forEach(moveDM);
            danmArrayTop.forEach(moveDM);
        }
        var top = 0.5;
        var fontSizeArr = [1.8, 2.2, 2.5];
        var tfsize = null;
        var bfsize = null;
        function createDanm() {
            danmArrayTop = danmArrayTop.filter(function (b) {
                return b.state === "run"
            });
            danmArrayBottom = danmArrayBottom.filter(function (b) {
                return b.state === "run"
            });
            var topDm = createDmElement(tfsize, top, topContainer);
            var t = topDm.el;
            danmArrayTop.push(new danm(t, movPx, -topDm.width));
            var bottomDm = createDmElement(bfsize, top, bottomContainer);
            var b = bottomDm.el;
            danmArrayBottom.push(new danm(b, movPx, -bottomDm.width));
            top += 4;
            top = top > 12 ? .5 : top;
        }
        function createDmElement(fsize, top, container) {
            var t = document.createElement('span');
            t.className = "dan-m-span";
            t.textContent = tanm[startPosition];
            startPosition += 1;
            startPosition %= tanm.length;//100;
            t.style.display = "none";
            var tsize = 0;
            if (t.textContent.length < 20) {
                tsize = Math.floor((Math.random() * 10) % 3);
            }
            if (fsize === 2 && tsize === 2) {
                tsize = 0;
            }
            t.style.fontSize = fontSizeArr[tsize] + 'rem';
            t.style.top = top + 'rem';
            container.append(t);
            var twidth = $(t).width();
            // var bwidth = $(b).width();
            t.style.right = -twidth + "px";
            // b.style.right = -bwidth + "px";
            t.style.display = "block";
            return {
                el:t,
                size: tsize,
                width:twidth,
                txtLength: t.textContent.length
            }
        }
        function initPage() {
            setTimeout(function () {
                $(".dwn-download-center").removeClass("opacity0");
            }, 200);
            setTimeout(function () {
                $(".dwn-body-line .line-left").removeClass("opacity0");
            }, 500);
            setTimeout(function () {
                $(".dwn-body-line .line-right").removeClass("opacity0");
            }, 600);
            setTimeout(function () {
                $(".dwn-diamond-qr").removeClass("opacity0").addClass("qr-normal");
            }, 800);
            var resizeCancel = null;
            $(window).resize(function () {
                clearTimeout(resizeCancel);
                resizeCancel = setTimeout(function () {
                    calculateRemPx();
                }, 300)
            })
        }
        function initCartoon() {
            setTimeout(function () {
                $(".cartoon-start .cartoon-left .cartoon-figure").animate({"left": "20px"}, "normal", "swing", function () {
                    $(".cartoon-start").removeClass("cartoon-start")
                }).animate({left:0});
                $(".cartoon-start .cartoon-right .cartoon-figure").animate({"left": "-20px"}, "normal", "swing", function () {
                    $(".cartoon-start").removeClass("cartoon-start")
                }).animate({left:0});
            }, 1200);
        }
        function calculateRemPx() {
            var width = $(win).width();
            var height = $(win).height();
            if (width < 1000) {
                $(document.documentElement).css("font-size", "12px");
                return;
            }
            var ratio = width / height;
            var fontSize = 16;
            if (ratio >= 1.8) { // 以宽度为准
                fontSize = width / 100
            }
            else { //以高度为准
                fontSize = height / 55
            }
            $(document.documentElement).css("font-size",  fontSize + "px");
        }
    })(window, document);