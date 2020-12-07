
<center><h1> Féléves beszámoló</h1>
<h2> A WarCraft I játékkal játszó gépi intelligencia fejlesztése<h2></center>

### Előszó

A Warcraft nevű játékot a Blizzard fejlesztette ki a 1994-ben. A játék műfaját tekintve valós idejű stratégiai játék, mely hatalmas sikernek örvendett a maga idejében, és 2 folytatást is megélt. A kora ellenére ma is igazán élvezhető játék, amennyiben hozzászokunk a régies és egyszerű grafikához és idejétmúlt irányításhoz. Ugyanakkor pont az "egyszerűsége" miatt lehet jó választás rá mesterséges intelligenciát írni. A játékmenetet a "könnyű megtanulni, nehéz elsajátítani" elvet vallja.

### A játékról

A játékban 2 játszható faj közül választhatunk, az emberek és az orkok. Célunk az ellenség összes egységét és épületét megsemmisíteni mielőtt ezt ő tenné meg velünk. Kezdéskor csak néhány munkás áll rendelkezésre, városháza, farm és egy katona. Az épületeket és a katonákat/munkásokat nyersanyagokból lehet építeni és venni.
2 nyersanyag található a játékban, a fa és az arany. Ezeket a munkások tudják megszerezni, a fákat a közeli erdőből, az aranyat meg az aranybányákból. Mint látható, nem bonyolultak a szabályok, és az épületek meg az egységek listája sem túl hosszú, mégsem olyan könnyű legyőzni a gépi ellenfelet.
A kérdés már csak az, egy másik gépnek sikerül-e felülkerekednie az ellenfelen.

### Célok

A szakdolgozat célja, egy olyan mesterséges intelligencia létrehozása, amely képes szembeszállni a játék beépített intelligenciájával, és le is győzi azt. Mindezt úgy, hogy inputként megkapja a játék képét, mérlegel, eldönti mi legyen a következő lépés, majd outputként megadja hogy a kurzor mely pozíciókban mit csináljon. Ezt lehetőleg akár másodpercenként többször is végrehajtva. 

### Első lépések

A játék kora miatt futtatásához szükséges a dosbox nevű emulátor, ráadásul annak egy módosított változata, hogy képes legyen a képet x időnként automatikusan lementeni, továbbá fogadni az AI által adott üzenetet, és megfelelelően reagálni rá.
Első lépésként a [dosbox forráskódját](https://sourceforge.net/p/dosbox/code-0/HEAD/tree/dosbox/trunk/) kellett megszerezni , majd követni a [buildelési utasítást](https://www.dosbox.com/wiki/Building_DOSBox_with_Visual_Studio). Ez leírja hogyan kell lebuildelni a dosboxot és a hozzá tartozó függőségeket. Ezeknek a verziószáma is fontos a kompatibilitás miatt. Sajnos a buildelés nem ment zökkenőmentesen, ügyelni kellett hogy minden függőség 32 bites legyen, mert a dosbox is az. A képek készítéséért felelős programrész nem fordult le, és a hiba a Windows SDK-ban volt. Erre sokáig nem tudtam megoldást találni, majd egy régebbi SDK verziót választottam ki és úgy a fordítás sikeres volt.
A buildelés után meg kellett találni a dosbox mely részét érdemes módosítani/bővíteni ahhoz hogy a képet le tudjam menteni. Ezt a render.cpp-ben találtam meg, az EndUpdate függvény végére az alábbi kódot írtam, ami jelenleg 2 másodpercenként menti le a képet.
```c++
// render.cpp adattagjainak bővítése
int fpsCounter = 0; // Egy fps számláló, arra, hogy ne minden frame-ben hívódjon meg a kép lementése

...
//RENDER_EndUpdate függvény bővítése
time_t start = time(0); // jelenelgi idő lekérése

		std::stringstream sstr;
		sstr << start; // idő szöveggé alakítása 
		int time;
		std::istringstream(sstr.str()) >> time; //idő számmá alakítása
		
//itt lehet megadni milyen időközönként mentsen, és ellenőrzi 
//hogy az fps számláló nagyobb-e mint az fps szám amivel a program fut
		if (time %2 == 0 && fpsCounter >= render.src.fps) 
		{
			LOG_MSG(sstr.str().c_str());
			CaptureState |= CAPTURE_IMAGE; // a CaptureState változó beállítása képernyőképre

			// itt hívódik meg a képernyőt lementő függvény
			CAPTURE_AddImage(render.src.width==0?640:render.src.width, render.src.height==0?400:render.src.height, render.src.bpp, pitch,
				flags, fps, (Bit8u*)&scalerSourceCache, (Bit8u*)&render.pal.rgb);
			CaptureState = 0; // CaptureState alaphelyzet
			fpsCounter = 0; // fps számláló alaphelyzet
		}

		else
		{
			fpsCounter++;
		}
```

### Programok közötti kommunikáció

Mivel a mesterséges intelligenciát pythonban lenne érdemes megírni, de a dosbox kódja C++, így elengedhetetlen valamilyen módon kapcsolatot létesíteni a 2 program között futási időben. Erre a legjobb választásnak a [ZeroMQ](https://zeromq.org/) nevű library tűnik, mivel a használata viszonylag egyszerű, gyors és rengeteg programozási nyelvet támogat. Készítettem egy teszt programot, ahol egy C++ban írt program üzenetet küld és fogad egy Pythonban írt programtól, ami azt demózza hogy működik és használható, a dosboxba való integrálásra kész. Ez a demo egy oda vissza kommunikációt mutat be, ugyanakkor lehetséges hogy elegendő egy fogadó és egy küldő.

### Összefoglalás

A kezdeti buildelési nehézségek ellenére úgy gondolom jól halad a projekt, a képernyő kép lementése látványosan történik, folyamatosan frissül a fájl az új adatokkal, és amint a ZeroMQ integrálása is megtörténik, folytatható a munka a mesterséges intelligenciával.