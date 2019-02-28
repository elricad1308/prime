/**
* aloha.js
*
* Este script contiene los datos de la simulacion del experimento con
* el protocolo ALOHA.
*
* @author Jose Aguilar-Canepa
*/

/** 
* Estos datos corresponden a la resolucion de la cadena utilizando 
* el metodo de Gauss-Seidel.
*/
var gauss = [
  [0.0, 0.18926522298854886, 0.28713870228385135, 0.32300093664238005, 0.3230164073804063, 0.30291396190652475, 0.27312699371392773, 0.23922027557056655, 0.2052605011659822, 0.17405687899612154, 0.14644039007267698, 0.12230988164480394, 0.10027703176172857, 0.08202195112595273, 0.06678129319047287, 0.051601343650767705, 0.040179106004286466, 0.02789545286018206, 0.01708651427661867, 0.009322582302748515],
  [0.0, 0.2938281637420214, 0.3369021180815208, 0.3495842299375926, 0.3353989486475087, 0.3053434730540588, 0.2652924998399427, 0.22284808280089394, 0.17911161607472298, 0.13524340164607912, 0.09584954002111833, 0.060287126790754535, 0.03326994301565248, 0.01653502652610992, 0.006229117517775441, 0.0022823610012966933, 8.432423809402036E-4, 8.064531798023046E-4, 6.038625202514308E-4, 6.627178730021574E-4],
  [0.0, 0.37096192732766453, 0.37312802377567644, 0.36270053264434055, 0.3365909590481701, 0.299980600328709, 0.25791101359203544, 0.2128061259880059, 0.16659183795893948, 0.12151513292267796, 0.08280238692467029, 0.0501201816857036, 0.027011119912676147, 0.012202073080601717, 0.005068361114431187, 3.8135600937349993E-4, 6.768171206359031E-4, 3.6596589160932033E-4, 1.9308861681189052E-4, 4.3356560894509824E-4],
  [0.0, 0.36718333211022386, 0.3585174426861014, 0.3399915921988512, 0.3127103260653126, 0.2778613666230685, 0.23792379534717395, 0.19374785124793917, 0.15052853654656867, 0.10863589519946174, 0.07228903378631611, 0.04355922033345754, 0.02369696708075411, 0.010864698634666128, 0.004683581697645607, 2.3185977753314307E-4, 9.366749061745117E-4, 7.894228337171223E-4, 4.0138783824810397E-4, 5.802918715718879E-4],
  [0.0, 0.3178225975706925, 0.30551605811708954, 0.2875207751533538, 0.2653365232523011, 0.23520899270191847, 0.20221867925027429, 0.16676604606225787, 0.1301132492457888, 0.09514518117127993, 0.06390875645105816, 0.03829884331958421, 0.019334867672228258, 0.009911707874209218, 0.002352497979377294, 0.0013802330668742965, 7.437801323789091E-4, 1.1587055164378898E-4, 3.479820631525081E-4, 1.77875198156958E-4],
  [0.0, 0.2486428510814038, 0.237855103881715, 0.22440924609710514, 0.20669707426820183, 0.18609324952158132, 0.16222252731959225, 0.1350766718808985, 0.10717523345718143, 0.07932133669684885, 0.05402602032968289, 0.033526696283513326, 0.018282820439147616, 0.008297917623879438, 0.0026919760600907184, 5.479297561942625E-4, 1.5970454682043912E-5, 7.130633804405862E-4, 9.504961160642778E-4, 5.610753888121875E-4],
  [0.0, 0.18196866775092715, 0.17333961973858864, 0.16445169059241238, 0.1516798264532072, 0.13690061714404092, 0.12012962025061359, 0.1029871546878948, 0.08198316545912106, 0.06247238351366356, 0.043668282653314926, 0.02820444155616512, 0.015451749548989325, 0.006547949517002942, 0.0024203707459619045, 0.0013268777425352266, 8.225794876870902E-4, 6.972244848865257E-4, 7.743983017402891E-4, 9.982568017866493E-4],
  [0.0, 0.1246839557962915, 0.11785389110242694, 0.110970484335811, 0.10407159582941947, 0.09327737004735934, 0.08381758964688145, 0.07150582424292762, 0.059030052513425996, 0.04568985368499519, 0.033456136064583, 0.021436068614709064, 0.012077948117214007, 0.0063630478532300545, 0.0014415623976155977, 0.0014840115705598723, 0.001051196259067626, 6.921445187123532E-4, 3.755566470323703E-4, 8.897988239742767E-4],
  [0.0, 0.07991076634936374, 0.07502316517782588, 0.07028978955757276, 0.06634657971107902, 0.060770270663723, 0.054528579248082666, 0.04709544821483497, 0.039651342029893226, 0.03300869359845154, 0.0232451018354434, 0.01594064173048525, 0.009796477000680676, 0.004707872148427374, 0.0010825987997899922, 3.1040846140766997E-4, 6.570635216394407E-4, 8.162104797170736E-4, 8.512407961268078E-4, 1.8262422956938528E-4],
  [0.0, 0.04732113454260457, 0.04340321793546833, 0.04193713508837321, 0.038492282811792525, 0.03551861028413079, 0.03304075154174024, 0.028163974797060412, 0.025943449223809447, 0.02002727501415783, 0.01582136866864705, 0.012337721818064702, 0.007634025671478459, 0.0027304183570086692, 8.929015394169882E-4, 9.172097736966465E-4, 3.252140655449329E-4, 8.469614254610784E-4, 4.061775933703395E-4, 9.423184722864814E-4],
  [0.0, 0.026382534724828998, 0.02460806365623066, 0.022578138792842605, 0.021390891065881237, 0.02008501309471853, 0.01836934628492154, 0.015747310930389544, 0.015064745216232316, 0.011121578221896784, 0.010378712096649948, 0.007832567029677847, 0.005466219324046479, 0.0026179016556001082, 0.0021685585880114756, 2.3037009711155887E-4, 0.0010532084015077569, 9.737698868202557E-4, 1.0579592896117219E-4, 2.741515744979981E-4],
  [0.0, 0.011852720361183244, 0.012933249301344579, 0.011712954695206177, 0.010912707584281457, 0.010519456856153613, 0.008808014858926952, 0.007601868339308526, 0.007216935214361522, 0.006127947106802923, 0.006230620171414806, 0.0036296753238567207, 0.0037800323475925823, 0.0010418634826020044, 3.026342401799007E-4, 4.0856919422386774E-4, 1.1732675837017283E-4, 9.024134991614708E-4, 1.6936777637628677E-4, 3.445130720933443E-5],
  [0.0, 0.004989017318206957, 0.005257748790160575, 0.004961625825546603, 0.0050110218949741756, 0.004390196267056821, 0.004527948221003448, 0.003316575743908999, 0.003211594631861873, 0.0030876265990890154, 0.0027341965010996895, 0.0026694211304101037, 0.0016763369943420133, 0.0012485293820275539, 1.1070698738023705E-4, 5.11548086934196E-4, 4.877251255905767E-5, 4.0428679121712417E-4, 4.492438086730175E-4, 2.372987961948831E-5],
  [0.0, 0.0014601720031343338, 0.0021541909976416653, 0.001087407965710275, 0.0025527799561974344, 0.002384189145341223, 0.0010067479045984822, 6.406783882674942E-4, 9.294445139003256E-4, 0.0015180784698671816, 2.0605705130395094E-4, 0.0011596350734261736, 6.631281031766784E-4, 0.0014041414604480766, 1.0257451347196189E-4, 3.496280598009175E-4, 3.069504745470421E-4, 6.013954603814627E-4, 9.746614316524821E-4, 6.02950660089507E-4],
  [0.0, 4.5940672479031965E-4, 6.814302614904766E-6, 9.456321024542507E-4, 4.529389815212014E-4, 0.001305712697924277, 1.1427244141427623E-4, 0.0014254246506485526, 8.551055718167141E-4, 5.73142745279378E-4, 8.77071256580704E-4, 0.0011216308134937307, 7.102361394763781E-4, 1.1898458908629141E-4, 6.975557663007791E-4, 6.892361386584409E-4, 8.527510239630755E-5, 7.292764742315106E-4, 6.696872125460665E-4, 9.244012231455346E-4],
  [0.0, 1.2734731290946035E-4, 8.892770744715932E-5, 0.0011148314714754855, 4.5671587930884254E-4, 8.478139176447875E-4, 5.3220367428449925E-5, 0.001077194004240486, 2.1662666450488773E-4, 6.244191687554342E-4, 8.504102397446435E-4, 2.0991695893312088E-4, 9.158172010246575E-4, 1.5524094379102614E-4, 5.690755777762868E-4, 1.6943443071814286E-4, 5.662466422573601E-4, 9.402813251736397E-4, 6.493101296519667E-4, 2.1846878663952225E-4],
  [0.0, 2.7551613126391235E-4, 6.892971595455789E-5, 4.5960711541660926E-5, 5.870741811370936E-4, 8.646095374898082E-4, 3.4173875003005755E-4, 8.456724887830196E-4, 7.447858474310665E-4, 6.089091685272596E-4, 5.574870621283112E-4, 3.589937911933703E-4, 5.285225741280173E-4, 1.9723069538037823E-4, 3.941865601856095E-4, 3.5391032874887646E-4, 3.321764342701342E-4, 2.7154997549950637E-4, 7.048619658589913E-4, 8.278619527693944E-4],
  [0.0, 7.594818473836351E-5, 5.046794855222359E-4, 7.764076615860381E-4, 7.06618122856995E-5, 2.6070396344755734E-4, 9.726424161077485E-4, 1.9390886858015107E-4, 6.528839799620755E-4, 1.1752311060359421E-4, 8.68203615098179E-4, 8.32030928349392E-4, 2.6446787509446526E-4, 2.960768601430408E-4, 5.389579777144586E-4, 6.096364948931975E-5, 5.202693154692192E-4, 4.0525876118797433E-4, 8.686032352207444E-4, 9.305591416496154E-4],
  [0.0, 7.342782350348941E-4, 1.3789844099531233E-4, 3.079873450223205E-4, 8.238909252996019E-4, 9.115821953757584E-4, 7.102290253459191E-4, 5.286140343732967E-4, 1.346823787271175E-4, 4.4309812315115226E-4, 8.298537927363644E-4, 1.1766176989288398E-4, 9.661315509135738E-5, 3.2320109295022126E-4, 6.926627764885337E-5, 4.0802276766614616E-4, 8.622688678168339E-4, 1.8174548458006051E-4, 1.7767572049054157E-4, 1.4297235193109768E-4],
  [0.0, 6.740126094025247E-4, 3.6057883967624446E-4, 3.940109609475245E-4, 4.124157313014224E-5, 7.194514527386098E-5, 2.55438331965551E-4, 3.757993046753101E-4, 4.841326240080878E-4, 2.6158207676032336E-4, 1.2369339053994513E-4, 9.906645361377204E-4, 1.1657176922404162E-4, 6.046710657211164E-4, 2.923875338899747E-5, 1.8426801956903353E-4, 3.3584502087892774E-4, 3.714696148315626E-4, 2.2490622267197778E-5, 4.447041279520135E-4]
];

/**
* Estos datos corresponden a la resolucion de la cadena utilizando
* una simulacion de la cadena.
*/
var simulated = [
  [0.0, 0.18738814946835147, 0.28198841187000684, 0.3192551919823365, 0.3166889368062935, 0.3120482603277071, 0.2781816224907345, 0.23561719919850932, 0.2033898575217637, 0.16542102824810298, 0.15386540870761814, 0.12114094672732886, 0.10397534036131405, 0.07559251689178202, 0.06532859268602426, 0.05271636124090089, 0.04448934541194161, 0.02587513379768081, 0.02015944982176112, 0.010211230680791668],
  [0.0, 0.30107041102959703, 0.34570758444406663, 0.3435173564123415, 0.3320832510280436, 0.30912617770798645, 0.2565374498105118, 0.22585084129958694, 0.17311898189667083, 0.14376821097283385, 0.08964107092429159, 0.06262167191468336, 0.02950392038320613, 0.018697847171518775, 7.225596794473172E-4, 0.007516018856467929, 0.003504933053249256, 0.00535815686534644, 0.004725672444094268, 0.008552725941428193],
  [0.0, 0.3790933097299229, 0.3683356468464565, 0.371456213310392, 0.34381358056917516, 0.30957896951759684, 0.26364435234666705, 0.21327857860963612, 0.1626613635798777, 0.11795602629945288, 0.07906879499500882, 0.05305821124770422, 0.030603915368605107, 0.008573396425717798, 0.004281997766286037, 0.005110137808207819, 0.0046080491867515104, 0.002177555776405938, 4.6369564690229803E-4, 0.009230605070487858],
  [0.0, 0.3692355115617672, 0.36717079656400153, 0.3400170561369196, 0.312434505348788, 0.27913133532545414, 0.23239755103082188, 0.1929576712949511, 0.15012943621007746, 0.10078742964023965, 0.06741758221665671, 0.0350140232190433, 0.02308653593651895, 0.011142060599880616, 0.008878337941769369, 0.0052807460393363, 0.00968160713745262, 0.0018521798750988437, 0.007528775158177725, 0.007150717773698206],
  [0.0, 0.30723704345802066, 0.3047767896524267, 0.28942649140073534, 0.2652215851125268, 0.23509554451329626, 0.2028931075936022, 0.15963913073696495, 0.12287712858557368, 0.09236448490925685, 0.06095781405547137, 0.0290349947918541, 0.015530059900133534, 0.008643866763287716, 0.009041379350227353, 0.0020463999508274927, 0.008931798291729413, 0.00641031334621095, 0.0043047554669496425, 0.003855311565314164],
  [0.0, 0.25711021113921206, 0.24660512535812082, 0.218593378386776, 0.2064801185910672, 0.1953016392251971, 0.1540033752300179, 0.12931802169817527, 0.10085722497896146, 0.07783210659003495, 0.06234208305384888, 0.03438256028727205, 0.025252898630954267, 0.0017271262705619026, 0.005756793193586798, 0.006675608076843703, 0.008528198261252595, 3.3265592259354253E-4, 0.005157787303008774, 0.00732313888580819],
  [0.0, 0.1754790197197968, 0.17752021737316287, 0.15493641688814597, 0.14694696069862376, 0.13864077877445125, 0.12190314121345268, 0.10296287830344483, 0.09109709773590295, 0.0671963399229008, 0.047802822589689965, 0.03584093229551234, 0.0074377181633340115, 0.011258976510230187, 0.008927005521075337, 0.007330561587208383, 0.0027525379007231838, 0.0036817144763119777, 0.0032632619348191704, 0.0029255538624466397],
  [0.0, 0.11477802336832962, 0.12713515163014175, 0.10548946736244287, 0.10400057367293844, 0.08924061487460366, 0.09271614460882838, 0.06553691497027174, 0.06662025907453159, 0.04405341587734054, 0.03315072594788742, 0.01340160413123934, 0.006027584658860406, 0.014024762055534446, 4.581933643005732E-4, 0.005077054474298455, 0.0059534631376568364, 0.009147548370179856, 0.0019439707343456747, 0.006336449819028468],
  [0.0, 0.07155460562280762, 0.06913646759228248, 0.07121328205662504, 0.0668053449855405, 0.05210295517984616, 0.05486870044647643, 0.04547436832324288, 0.04656223517511246, 0.023969165266285564, 0.026742417980390915, 0.025295071866005846, 0.006709199590413394, 0.0035274480199883667, 0.011313674155783243, 0.004537503608038326, 2.0954047363250017E-5, 8.352278016546897E-4, 0.008139893553739405, 1.5366395629237405E-4],
  [0.0, 0.04258252527938284, 0.05186623362617089, 0.037735431193356546, 0.03508919547212375, 0.03141855145014932, 0.026883602980561472, 0.02339311755506515, 0.027878023997717282, 0.016181589304234016, 0.018669874583939927, 0.0022559466339986574, 0.013247112762718161, 0.010384965290963492, 0.0038890588560296347, 0.00356985708001929, 0.002349917922361448, 0.0013029774502665604, 0.004170160298240494, 0.008489813765913179],
  [0.0, 0.031296501349993254, 0.01609544078460178, 0.030201503884615052, 0.02980852235268873, 0.027777473012378227, 0.01829562664947878, 0.020415827854129206, 0.021911389655934206, 0.01819911416478704, 0.008514657173701649, 0.0038409889480100707, 2.477639268598994E-4, 6.542774111072888E-4, 0.0018474398574164614, 0.003411407013647219, 0.007754292244045226, 0.007817761054244627, 0.006369441619177612, 0.006290271750200068],
  [0.0, 0.0170787408079334, 0.020598145980786402, 0.010632348725267683, 0.011179270312873314, 8.703126686998072E-4, 0.01642531595617594, 0.004238358463153304, 0.001411092602059758, 0.010707429417287292, 0.001093114377688287, 0.013878189189210506, 0.010963118098054614, 0.0044626571506540345, 0.004254269797247214, 0.006735996049554253, 0.00920970852964437, 9.935563941750089E-4, 0.0017914296341013276, 0.002636113761783418],
  [0.0, 0.011212215406478581, 0.005796399475529496, 0.0043709985705365495, 0.007005660233514167, 0.013867642844119704, 0.00469524680765711, 0.011390999088780761, 0.001232245011779202, 0.005412842032561923, 0.003077180312025684, 0.005637050245625745, 0.00238812674543831, 0.006344123352916216, 0.005257684731264703, 0.009301969983637103, 0.00789728452036457, 0.0012466381540204195, 0.0065646683249071984, 0.009789917759454897],
  [0.0, 4.245088823046884E-4, 2.539777119381988E-4, 0.0015302530537768268, 0.009937559766048692, 0.006331374959422032, 0.0024631213786456573, 0.008451628757290908, 0.009314147921430066, 0.005255555325940473, 0.0060369081245623575, 0.010607561867916124, 0.0056860446765015366, 0.002940221905087924, 0.010227296424694988, 0.007699204322446162, 0.0043016952969685655, 8.342107011854654E-4, 0.002058420209249036, 0.0022421005721261645],
  [0.0, 0.010475956507363231, 0.0080235415654476, 0.005864511728998323, 8.7707575804402E-4, 0.009049506262917263, 0.0010339416876608662, 0.007664260852482033, 0.009759794139231375, 0.0068605935581320596, 0.007114245601788247, 0.0022247583489323785, 0.008556357600449453, 0.006927519188620537, 8.752680895109299E-4, 0.006298792571044166, 0.0039062045380654302, 0.002261267634711897, 0.007483128161323277, 0.0025157327719550625],
  [0.0, 0.006517457712679419, 0.0019274107052167876, 3.8208262639613023E-4, 0.009761105715481846, 0.003220971160099211, 0.005812088054778179, 0.007424231435199862, 0.0019997979179664296, 0.0069476489125954435, 0.006423058573519708, 0.0056119356934867266, 0.0014604116953179692, 0.0032810718063559646, 0.00780331646059534, 0.0026299739936572857, 0.0020033789429856207, 0.0059958357748278335, 6.217294970813656E-5, 0.00298756772109955],
  [0.0, 0.008652910601938596, 0.00990352650319523, 0.0015702735114528602, 0.006508956503865809, 0.006890618139036988, 0.00958130290399029, 0.009372953762558695, 0.009227865551970178, 0.005933608635561, 0.0035810090519385563, 0.00993789993752325, 0.004537320626976326, 0.0021533058374136626, 0.0050137350407725035, 0.009408417960908608, 0.0029118775233906323, 0.002836265861406783, 0.006400578479971595, 0.005483113917225013],
  [0.0, 0.0010780524361034911, 0.0011085953441803502, 0.00260877265648736, 0.006458706404389169, 0.003943362799193009, 0.00545464752218974, 0.0035017362829743953, 0.006845911532316243, 0.005446231218394321, 0.0031194427761329475, 0.009532235607406885, 0.008277895019802143, 0.008086505707587087, 0.006425510760173996, 0.0050023840603560825, 0.006677631022485094, 0.009263195482571138, 0.0011934484403993465, 0.002903589257556038],
  [0.0, 0.0013352617452094106, 0.004792281617523534, 0.00208897622445632, 0.0025544276514966563, 0.0066058174764028355, 0.00918802314514634, 0.008520498620136872, 0.009945798754031336, 0.0010502755549800695, 0.00343086935161357, 0.0055458240914487275, 0.005839075746736062, 0.0030484970441431217, 0.0024968864755475014, 7.842461417234346E-4, 0.003168732508941848, 0.005922725872076353, 0.0018984823290545347, 0.009642519731771987],
  [0.0, 0.005572023072621758, 0.009975901392749294, 0.008010609876968501, 0.008558175577522639, 0.0069863905015452735, 0.002282838900759026, 0.009169251422083741, 0.005302221070044324, 0.005933491622685692, 0.004982376341970984, 0.00245219059868736, 0.0024960967996404426, 0.0046058470516392724, 0.006666141096528009, 0.00370070359146281, 0.009652728638139105, 0.002517569219676731, 5.109806916396226E-4, 4.98416908410096E-5]
];

/**
* Estos datos corresponden a la resolucion de la cadena de manera
* directa.
*/
var direct = [
  [0.0, 0.1896163751286022, 0.286497566192988, 0.3226351254593103, 0.3230357297200504, 0.3022860054683482, 0.2728569042929421, 0.23855326203844193, 0.20526277026550613, 0.1738794403717531, 0.14676053603643413, 0.12149961115076179, 0.10106628155166708, 0.08206480260812017, 0.06594710349534522, 0.051632341154080996, 0.03866492265428689, 0.027846967263060907, 0.01677775251734548, 0.007627544574906725],
  [0.0, 0.29425621587603806, 0.3368182966496043, 0.3486239052106645, 0.33439630855090063, 0.303795355323907, 0.26559830552241465, 0.22215114345912604, 0.17865154611706047, 0.13554864953276008, 0.09577337298423354, 0.06033087410570435, 0.033511220823208905, 0.014956791940376829, 0.005743040970133562, 0.0013231263253412069, 5.481618697774141E-4, 8.929609600007511E-4, 7.301945640867063E-4, 3.8610099134560603E-4],
  [0.0, 0.36977995697737753, 0.3725176018697133, 0.36161634288025535, 0.33681842660139294, 0.3003536830480033, 0.257665959775528, 0.21156355415781897, 0.16548180293221745, 0.12094129375169106, 0.08173094062201317, 0.04891654224963525, 0.026309340979762508, 0.011051001004294668, 0.0042783260327538646, 6.435934476109024E-4, 7.259854253714234E-4, 4.908570015630749E-4, 2.3640555073794505E-4, 1.578122755699295E-4],
  [0.0, 0.36721828699141035, 0.3573391225780334, 0.3395793261400564, 0.3116131122147255, 0.2766458456034821, 0.2364775570617866, 0.19373963356276344, 0.15014680690628257, 0.10883038525071391, 0.07222710037224175, 0.04345587338082248, 0.021911323900166722, 0.00939213082619244, 0.0037130962975497487, 0.001040363466961797, 3.880185423795101E-4, 1.1792030055023271E-4, 6.626587575138372E-4, 9.619664436376332E-4],
  [0.0, 0.316054933275233, 0.3043994671647104, 0.28724555784999745, 0.26439876868086387, 0.23590271538201216, 0.20244162607776067, 0.16672871294355768, 0.1299875913422272, 0.09503556647107132, 0.06338272125497343, 0.03721086996354603, 0.0196013661430065, 0.008054531066306582, 0.003045333453423743, 6.435527978631282E-4, 1.7278257423621678E-4, 7.120090992676729E-4, 6.376517866158135E-4, 2.2867203562513267E-4],
  [0.0, 0.2488914196017511, 0.23860096438109862, 0.2245748085952412, 0.20649955921753282, 0.18547620069861795, 0.16138177656952285, 0.13472571459857574, 0.10627044330204968, 0.07926372239873083, 0.05343359702581036, 0.032478547753495686, 0.017236055237925332, 0.007419307403856277, 0.002101032538813506, 6.51426782888879E-4, 8.291521872935734E-4, 4.015273404071807E-4, 7.805671148568005E-4, 6.11734686275444E-5],
  [0.0, 0.18136380107706035, 0.17329904686850822, 0.16331382178263623, 0.1503196025045074, 0.13656963285269103, 0.12008682862553136, 0.10151279986068236, 0.08237899897908642, 0.06179022073226824, 0.0433845274865839, 0.0270026439379831, 0.014416521638883902, 0.0059050089706296225, 0.0019344610414020861, 2.4819196610506545E-4, 6.840645690548117E-4, 7.781863182336928E-4, 1.362813471686074E-4, 4.2511120863315393E-4],
  [0.0, 0.12311234916194697, 0.11766115690969074, 0.11041343245992025, 0.10297837962200504, 0.09402941004259138, 0.08343687578468832, 0.07186240506095443, 0.058851880804196684, 0.045874178236417824, 0.03296064496341239, 0.020925036717768283, 0.011464742410027054, 0.005045616036363945, 0.0014912133785710087, 3.63417471190896E-4, 4.265879508101089E-4, 5.531384946272761E-4, 8.904252680150418E-4, 4.252418816969863E-4],
  [0.0, 0.07825812112569536, 0.07495814594908992, 0.0705950535713616, 0.06573059696521254, 0.06004105657323463, 0.05383297265222221, 0.047577302163475776, 0.039504571632077254, 0.03185834232664523, 0.024077194979166012, 0.015547912420251735, 0.009211721888858947, 0.003827267511954377, 0.0017598649301778606, 4.417628369026042E-4, 8.403100619787254E-4, 7.732415795407457E-4, 6.495752487086762E-4, 6.923544588045203E-4],
  [0.0, 0.04638002193624623, 0.04364611714648098, 0.0409227829291689, 0.03886396352887676, 0.03590967351855817, 0.03203323509281238, 0.02830008250779246, 0.024556876771635504, 0.020147042151588336, 0.015497101235282588, 0.010787201935242217, 0.006705077432921092, 0.002760776505153365, 0.0014291643482017597, 1.3647506547765335E-4, 2.99202513161582E-4, 2.9279238000057116E-4, 7.250933589624775E-4, 5.017510401242332E-4],
  [0.0, 0.02499963388379612, 0.023604064585472876, 0.02221177011780235, 0.020307790693499906, 0.019174601645061143, 0.017822955187708947, 0.015219028067946332, 0.01329405884571276, 0.011781809584593343, 0.009462542201109892, 0.007065416401613375, 0.004249440114171085, 0.002096352962269932, 3.198599119693217E-4, 7.751917512666319E-5, 8.218550441778447E-4, 7.476348987767365E-4, 2.93695791800072E-4, 3.745432379788802E-4],
  [0.0, 0.012580041881575249, 0.01109003649024943, 0.010563209655775103, 0.010456828385000607, 0.009452100554514878, 0.00855670610050286, 0.008051372762583126, 0.006455188152745842, 0.005683342960083984, 0.00479789772956411, 0.0036001019395600774, 0.0026026498365964213, 0.0014209362890066177, 8.067840300914326E-4, 2.498189217665495E-4, 2.4135509207549665E-4, 8.61520622158484E-4, 2.364773963413478E-5, 5.741484193381242E-4],
  [0.0, 0.004953375893700781, 0.004576936338623034, 0.004792491992082817, 0.00374047507401538, 0.004132639099689838, 0.0036913496833422136, 0.003261532258986273, 0.0033097036985455528, 0.002838861481902636, 0.002365415109461595, 0.001731752399360846, 7.734091980976088E-4, 6.642742856621401E-4, 1.0678503119120687E-4, 1.2714724474442585E-4, 5.919422538152926E-4, 5.288475267532902E-4, 7.525530140851695E-4, 1.0275264813338042E-4],
  [0.0, 0.0020122696836753296, 0.001932114899100562, 0.0013965315044506214, 0.0016136526866118645, 0.0016570091656551347, 0.0011494821215200575, 4.7269303208105184E-4, 3.2659133935249813E-4, 8.079223956912791E-4, 7.629978725920513E-4, 7.820040355007558E-5, 2.561608777501531E-4, 2.9597778779445164E-4, 3.1877533439433496E-4, 4.849906620607877E-4, 1.3868435479430513E-4, 7.634102995601881E-4, 8.102662872095788E-5, 5.261396575150143E-4],
  [0.0, 4.43256217691402E-4, 4.658403194080614E-4, 7.691570990237613E-5, 1.752913219905906E-5, 3.403285985572362E-4, 2.051118765380338E-4, 4.7709562798286127E-4, 4.5809627358588524E-4, 9.200758550195157E-6, 1.9267080903824063E-4, 1.793260599658095E-4, 4.59776881881356E-4, 7.455968186413937E-4, 9.002821383247529E-5, 1.1542176445005132E-4, 5.82683637939642E-4, 2.7954851740134504E-4, 3.0610929314826027E-4, 2.101688630171443E-4],
  [0.0, 7.80179795637964E-4, 8.216622177936114E-4, 3.048942451679698E-4, 3.63697483994556E-5, 1.892186566667921E-4, 5.262534501655794E-4, 3.9534278779330197E-4, 7.923022424648792E-4, 7.747682389969189E-4, 2.369295728954638E-4, 6.496855411619933E-4, 6.958139423726349E-4, 1.0780145423137079E-4, 5.379567794104536E-4, 1.2697511759497562E-4, 8.618695425342356E-4, 1.8007057670733418E-4, 9.591027693880382E-4, 3.3831727434624183E-4],
  [0.0, 5.238564852438414E-4, 9.458548870313466E-4, 1.403737415516494E-4, 2.872776323031863E-4, 3.089995966968264E-4, 4.5141069238922864E-5, 6.241318521853562E-4, 1.325253673084698E-5, 5.783053247026165E-4, 4.8640266659232657E-4, 3.212817077105875E-5, 5.894771035105139E-4, 1.4114657499470222E-4, 6.823859607860828E-4, 6.227877265582045E-4, 6.380395200574907E-4, 9.645065096879924E-4, 3.345753800300645E-4, 3.970834246711354E-4],
  [0.0, 7.667369088336677E-4, 5.292636561159758E-4, 8.811311732491797E-4, 9.627970437088652E-4, 5.168963698743203E-4, 3.2529293160258563E-4, 1.8286741347679368E-4, 9.356293779508577E-4, 9.564236761035203E-4, 1.4908314491671483E-4, 6.446009654863092E-4, 6.233211941504768E-4, 5.998891201734095E-4, 2.870168697147028E-4, 7.421280502264868E-4, 1.3562043223130348E-5, 8.417982795166814E-4, 8.006054958429047E-4, 6.64684592520324E-4],
  [0.0, 7.491280450610724E-4, 2.914109976377741E-4, 4.054500069022745E-5, 7.244407176706786E-4, 3.3465630465897704E-4, 5.366418653291026E-4, 6.129263058856129E-5, 1.15595956056197E-4, 7.406881925244163E-4, 2.779622592764553E-4, 9.700996715680901E-4, 7.00910545441315E-4, 8.307199076993266E-4, 4.074068791981058E-4, 5.31560652955027E-4, 2.4281750932067793E-4, 1.3440327424544423E-4, 3.648807573831967E-4, 6.183605583314377E-4],
  [0.0, 9.583081499211969E-4, 8.174213330957632E-4, 5.009617244040297E-4, 6.802347269358243E-4, 7.456186773970416E-4, 5.921254992332316E-4, 7.733894692714898E-4, 2.0037682755846422E-5, 4.443517273970064E-4, 3.9383044312904796E-4, 1.0257260453960024E-4, 2.7018960828698014E-4, 7.267557203879881E-4, 5.502002920768471E-5, 1.50690246869959E-4, 2.1660317896027978E-4, 3.9194340944675196E-4, 9.371741058918155E-4, 8.673074612815518E-5]
];

// Transformamos los datos al formato requerido por Plotly.
var data = [
  { 
    z : gauss, 
    visible : true,
    type : 'surface', 
    opacity : 0.75,
    name : 'Gauss-Seidel',
    colorscale : 'Rainbow',
    showscale : false
  },

  { 
    visible : true,
    z : simulated, 
    type : 'surface', 
    opacity : 0.75,
    name : 'Simulation',
    colorscale : 'Picnic',
    showscale : false
  },

  { 
    visible : true,
    z : direct,
    type : 'surface', 
    opacity : 0.75,
    name : 'Direct',
    colorscale : 'Earth',
    showscale : false
  }
];

var layout = {
      title : 'Throughput of an ALOHA protocol simulation',
      width : 994,
      height : 600,

      scene : {
            xaxis : {
                  title : '\u03c3',
                  type : 'linear',
                  tickmode : 'array',
                  tickvals : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
                  ticktext : [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                  ticks : 'inside',
                  mirror : false
            }, 

            yaxis : {
                  title : '\u03c4',
                  type : 'linear',
                  tickmode : 'array',                  
                  tickvals : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
                  ticktext : [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                  ticks : 'outside',
                  mirror : false
            },

            zaxis : {
                  title : 'Throughput'
            }
      }
}

// Creamos el widget para visualizar los datos.
Plotly.plot('experiment', data, layout);

// Agregamos los eventos para mostrar/ocultar a los botones
$('.control-div button').click(function() {
      var index = -1;

      if(this.id === 'gauss') 
            index = 0;
      else if (this.id === 'sim') 
            index = 1;
      else if (this.id === 'direct') 
            index = 2;
      else 
            index = -1;

      if(index === -1) {
            console.warn('Unknown id: ' + this.id);
            return;
      } else {
            plot = document.getElementById('experiment');
            var op = plot.data[index].opacity;

            if(op === undefined) op = 1.0;

            var update = {
                  opacity : (op === 1 ? 0.75 : 1.0)
            }

            Plotly.restyle(plot, update, index);
      }
});