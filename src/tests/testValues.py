import pandas as pd

class TestValue:
    klines1 = [[1615291200000, 54274.0, 54834.0, 53606.0, 54153.0, 382259.0], [1615305600000, 54219.0, 54379.0, 53661.0, 54129.0, 305719.0], [1615320000000, 54127.0, 54913.0, 53920.0, 54893.0, 957932.0], [1615334400000, 54893.0, 55825.0, 53200.0, 53494.0, 1590035.0], [1615348800000, 53538.0, 54445.0, 53090.0, 54223.0, 595907.0], [1615363200000, 54232.0, 55512.0, 54100.0, 54889.0, 396763.0], [1615377600000, 54899.0, 56527.0, 54852.0, 56344.0, 671089.0], [1615392000000, 56335.0, 57433.0, 56102.0, 56776.0, 827287.0], [1615406400000, 56798.0, 57320.0, 55604.0, 55930.0, 694332.0], [1615420800000, 55959.0, 56587.0, 55271.0, 56041.0, 511981.0], [1615435200000, 56026.0, 56262.0, 55082.0, 55100.0, 592893.0], [1615449600000, 55125.0, 56285.0, 54330.0, 56223.0, 566217.0], [1615464000000, 56249.0, 57289.0, 55794.0, 56346.0, 1240856.0], [1615478400000, 56348.0, 57763.0, 56303.0, 56829.0, 885852.0], [1615492800000, 56869.0, 58213.0, 56564.0, 57794.0, 894201.0], [1615507200000, 57812.0, 58111.0, 56700.0, 57173.0, 544966.0], [1615521600000, 57150.0, 57495.0, 56400.0, 56758.0, 416555.0], [1615536000000, 56754.0, 57154.0, 55859.0, 56468.0, 465627.0], [1615550400000, 56503.0, 57162.0, 55090.0, 56988.0, 1298401.0], [1615564800000, 56998.0, 57776.0, 56736.0, 56952.0, 828591.0], [1615579200000, 56954.0, 57548.0, 56300.0, 57322.0, 573885.0], [1615593600000, 57353.0, 57362.0, 56130.0, 56709.0, 350969.0], [1615608000000, 56707.0, 57473.0, 56292.0, 57425.0, 1391142.0], [1615622400000, 57424.0, 60334.0, 57138.0, 59910.0, 2432282.0], [1615636800000, 59918.0, 60499.0, 59291.0, 59719.0, 809250.0], [1615651200000, 59725.0, 60870.0, 59489.0, 60765.0, 888854.0], [1615665600000, 60768.0, 61910.0, 60699.0, 61249.0, 1474951.0], [1615680000000, 61250.0, 61742.0, 60792.0, 61356.0, 1177156.0], [1615694400000, 61352.0, 61517.0, 60534.0, 60565.0, 664503.0], [1615708800000, 60564.0, 61175.0, 59460.0, 60398.0, 1239456.0], [1615723200000, 60359.0, 60634.0, 59566.0, 59781.0, 313712.0], [1615737600000, 59781.0, 60463.0, 59379.0, 59996.0, 285756.0], [1615752000000, 59996.0, 60798.0, 58965.0, 58999.0, 1845054.0], [1615766400000, 58958.0, 60534.0, 58756.0, 60410.0, 707757.0], [1615780800000, 60431.0, 60708.0, 57336.0, 57881.0, 1497949.0], [1615795200000, 57880.0, 58434.0, 54400.0, 56151.0, 3009066.0], [1615809600000, 56143.0, 57286.0, 55090.0, 56231.0, 1658860.0], [1615824000000, 56233.0, 56692.0, 55500.0, 56585.0, 794653.0], [1615838400000, 56574.0, 56940.0, 55587.0, 55680.0, 511996.0], [1615852800000, 55651.0, 56101.0, 53337.0, 54323.0, 1409401.0], [1615867200000, 54324.0, 55494.0, 53676.0, 55272.0, 682230.0], [1615881600000, 55262.0, 56424.0, 55155.0, 55474.0, 342495.0], [1615896000000, 55508.0, 55951.0, 54701.0, 55881.0, 1025848.0], [1615910400000, 55881.0, 56130.0, 55011.0, 55778.0, 1364937.0], [1615924800000, 55763.0, 56932.0, 55734.0, 56907.0, 1032990.0], [1615939200000, 56913.0, 57198.0, 55450.0, 55515.0, 846115.0], [1615953600000, 55525.0, 56350.0, 55256.0, 55861.0, 516858.0], [1615968000000, 55860.0, 56102.0, 54448.0, 54841.0, 1039071.0], [1615982400000, 54865.0, 55452.0, 54177.0, 54983.0, 1388614.0], [1615996800000, 54978.0, 58179.0, 54798.0, 57853.0, 1448611.0], [1616011200000, 57866.0, 58965.0, 57586.0, 58883.0, 1540696.0], [1616025600000, 58884.0, 59536.0, 58655.0, 58778.0, 824648.0], [1616040000000, 58802.0, 59249.0, 58171.0, 58408.0, 926630.0], [1616054400000, 58398.0, 58721.0, 57950.0, 58218.0, 448501.0], [1616068800000, 58194.0, 59664.0, 57569.0, 59530.0, 1125850.0], [1616083200000, 59598.0, 60130.0, 57266.0, 57317.0, 1455113.0], [1616097600000, 57333.0, 58140.0, 57031.0, 57652.0, 1207199.0], [1616112000000, 57652.0, 57888.0, 56302.0, 57780.0, 537160.0], [1616126400000, 57800.0, 58495.0, 57606.0, 57810.0, 626190.0], [1616140800000, 57865.0, 58905.0, 57525.0, 58821.0, 439605.0], [1616155200000, 58850.0, 59268.0, 57978.0, 59014.0, 839858.0], [1616169600000, 59047.0, 59212.0, 58389.0, 58869.0, 1023873.0], [1616184000000, 58891.0, 59500.0, 58044.0, 58092.0, 1092950.0], [1616198400000, 58050.0, 58971.0, 57856.0, 58475.0, 561400.0], [1616212800000, 58475.0, 58651.0, 58034.0, 58473.0, 272265.0], [1616227200000, 58479.0, 59370.0, 58479.0, 59316.0, 221259.0], [1616241600000, 59352.0, 59948.0, 58638.0, 59266.0, 883732.0], [1616256000000, 59331.0, 59482.0, 58953.0, 59301.0, 267801.0], [1616270400000, 59312.0, 59403.0, 58050.0, 58145.0, 780577.0], [1616284800000, 58121.0, 58599.0, 57469.0, 57798.0, 591622.0], [1616299200000, 57765.0, 57811.0, 56710.0, 57061.0, 1363223.0], [1616313600000, 57001.0, 57387.0, 55470.0, 56257.0, 782822.0], [1616328000000, 56220.0, 57562.0, 55917.0, 57199.0, 1449883.0], [1616342400000, 57175.0, 57698.0, 56744.0, 57540.0, 835530.0], [1616356800000, 57550.0, 58166.0, 57238.0, 57410.0, 793689.0], [1616371200000, 57390.0, 57699.0, 56347.0, 57607.0, 931695.0], [1616385600000, 57633.0, 57926.0, 57358.0, 57636.0, 340922.0], [1616400000000, 57633.0, 58505.0, 57114.0, 57769.0, 339566.0], [1616414400000, 57781.0, 57822.0, 56601.0, 57094.0, 1188973.0], [1616428800000, 57104.0, 57240.0, 55526.0, 55582.0, 785383.0], [1616443200000, 55566.0, 56055.0, 53400.0, 54106.0, 1889210.0], [1616457600000, 54109.0, 55325.0, 53826.0, 54678.0, 905705.0], [1616472000000, 54688.0, 54803.0, 52989.0, 54218.0, 1316059.0], [1616486400000, 54218.0, 54850.0, 53008.0, 54249.0, 1077253.0], [1616500800000, 54287.0, 55498.0, 54287.0, 55243.0, 1366731.0], [1616515200000, 55251.0, 55833.0, 54877.0, 55050.0, 928829.0], [1616529600000, 55022.0, 55111.0, 54250.0, 54432.0, 786729.0], [1616544000000, 54409.0, 54828.0, 53601.0, 54442.0, 874511.0], [1616558400000, 54400.0, 55638.0, 53753.0, 55522.0, 1429530.0], [1616572800000, 55476.0, 56713.0, 55474.0, 56567.0, 1451850.0], [1616587200000, 56575.0, 57192.0, 56084.0, 56344.0, 765786.0], [1616601600000, 56406.0, 56472.0, 54732.0, 54807.0, 1250362.0], [1616616000000, 54784.0, 54784.0, 51714.0, 52307.0, 2090776.0], [1616630400000, 52304.0, 52827.0, 51520.0, 52140.0, 2282302.0], [1616644800000, 52141.0, 53229.0, 51935.0, 52276.0, 1427792.0], [1616659200000, 52286.0, 53136.0, 52102.0, 52200.0, 1501959.0], [1616673600000, 52184.0, 52369.0, 50510.0, 50994.0, 3254369.0], [1616688000000, 51013.0, 52580.0, 50600.0, 52196.0, 1825074.0], [1616702400000, 52219.0, 52732.0, 51260.0, 51351.0, 985713.0], [1616716800000, 51345.0, 52722.0, 51269.0, 52420.0, 1549119.0], [1616731200000, 52459.0, 53560.0, 52215.0, 53524.0, 1099256.0], [1616745600000, 53558.0, 53820.0, 52621.0, 52761.0, 1821044.0], [1616760000000, 52771.0, 53543.0, 52576.0, 53295.0, 1408975.0], [1616774400000, 53324.0, 54035.0, 52905.0, 53757.0, 1954470.0], [1616788800000, 53773.0, 55077.0, 53773.0, 55049.0, 2116912.0], [1616803200000, 55049.0, 55550.0, 54515.0, 54776.0, 1592307.0], [1616817600000, 54818.0, 55359.0, 54673.0, 54983.0, 817641.0], [1616832000000, 54974.0, 55162.0, 54329.0, 54467.0, 936485.0], [1616846400000, 54478.0, 55039.0, 54010.0, 54990.0, 1369094.0], [1616860800000, 54987.0, 56292.0, 54987.0, 55798.0, 1161177.0], [1616875200000, 55792.0, 56639.0, 55710.0, 55820.0, 1317500.0], [1616889600000, 55806.0, 56180.0, 55566.0, 56031.0, 1294648.0], [1616904000000, 56029.0, 56460.0, 55850.0, 56207.0, 238459.0], [1616918400000, 56208.0, 56562.0, 55700.0, 55822.0, 612525.0], [1616932800000, 55809.0, 56396.0, 55315.0, 56380.0, 1088961.0], [1616947200000, 56376.0, 56489.0, 54700.0, 55185.0, 1756935.0], [1616961600000, 55214.0, 55885.0, 54801.0, 55797.0, 1694041.0], [1616976000000, 55800.0, 55931.0, 55013.0, 55374.0, 1552450.0], [1616990400000, 55380.0, 56187.0, 54944.0, 55920.0, 1275576.0], [1617004800000, 55930.0, 58350.0, 55873.0, 57862.0, 1327142.0], [1617019200000, 57900.0, 58449.0, 57301.0, 57725.0, 1166521.0], [1617033600000, 57730.0, 58350.0, 57225.0, 57676.0, 789824.0], [1617048000000, 57699.0, 57950.0, 57138.0, 57689.0, 1176567.0], [1617062400000, 57688.0, 57798.0, 57193.0, 57266.0, 1029037.0], [1617076800000, 57261.0, 58336.0, 57153.0, 58167.0, 1808843.0], [1617091200000, 58168.0, 59427.0, 57762.0, 59286.0, 1822415.0], [1617105600000, 59296.0, 59463.0, 58622.0, 58651.0, 1021702.0], [1617120000000, 58650.0, 59229.0, 58600.0, 59131.0, 836234.0], [1617134400000, 59130.0, 59153.0, 58431.0, 58815.0, 1704417.0], [1617148800000, 58813.0, 59090.0, 58416.0, 58650.0, 944926.0], [1617163200000, 58659.0, 59939.0, 57332.0, 58199.0, 2058915.0], [1617177600000, 58284.0, 58359.0, 56856.0, 58101.0, 2530745.0], [1617192000000, 58101.0, 59494.0, 57765.0, 59367.0, 1888152.0], [1617206400000, 59343.0, 59719.0, 58465.0, 58671.0, 1927467.0], [1617220800000, 58689.0, 59426.0, 58415.0, 58875.0, 1315482.0], [1617235200000, 58875.0, 59400.0, 58857.0, 59200.0, 844829.0], [1617249600000, 59200.0, 59295.0, 58579.0, 58900.0, 1981415.0], [1617264000000, 58900.0, 59520.0, 58068.0, 58597.0, 1052067.0], [1617278400000, 58596.0, 59339.0, 58427.0, 59046.0, 1199370.0], [1617292800000, 59047.0, 59213.0, 58017.0, 58976.0, 1456603.0], [1617307200000, 58976.0, 59121.0, 58604.0, 58828.0, 1087958.0], [1617321600000, 58857.0, 60381.0, 58528.0, 59949.0, 1819809.0], [1617336000000, 59950.0, 60073.0, 59453.0, 59560.0, 1472870.0], [1617350400000, 59555.0, 59759.0, 59314.0, 59619.0, 1003762.0], [1617364800000, 59620.0, 59718.0, 59085.0, 59567.0, 1520980.0], [1617379200000, 59567.0, 59673.0, 58555.0, 58887.0, 606436.0], [1617393600000, 58890.0, 59303.0, 58580.0, 59069.0, 786042.0], [1617408000000, 59062.0, 59500.0, 59013.0, 59295.0, 596721.0], [1617422400000, 59286.0, 59655.0, 59265.0, 59403.0, 1167682.0], [1617436800000, 59428.0, 59890.0, 58851.0, 59353.0, 638400.0], [1617451200000, 59345.0, 59578.0, 58901.0, 58901.0, 1279487.0], [1617465600000, 58905.0, 59202.0, 57833.0, 58629.0, 1271374.0], [1617480000000, 58612.0, 58612.0, 56930.0, 57147.0, 1076625.0], [1617494400000, 57137.0, 57611.0, 56521.0, 57539.0, 1218697.0], [1617508800000, 57524.0, 57722.0, 57236.0, 57650.0, 622248.0], [1617523200000, 57692.0, 57800.0, 57183.0, 57302.0, 255981.0], [1617537600000, 57314.0, 58572.0, 57073.0, 57960.0, 1060653.0], [1617552000000, 57970.0, 58295.0, 57718.0, 57998.0, 606725.0], [1617566400000, 57998.0, 58333.0, 57900.0, 58242.0, 431293.0], [1617580800000, 58266.0, 58456.0, 57405.0, 57567.0, 358154.0], [1617595200000, 57567.0, 57675.0, 56842.0, 57332.0, 702245.0], [1617609600000, 57306.0, 57779.0, 56821.0, 57772.0, 265434.0], [1617624000000, 57779.0, 59339.0, 57779.0, 59052.0, 844655.0], [1617638400000, 59077.0, 59289.0, 58703.0, 59112.0, 873172.0], [1617652800000, 59106.0, 59247.0, 58618.0, 59247.0, 477498.0], [1617667200000, 59246.0, 59600.0, 58712.0, 58823.0, 897297.0], [1617681600000, 58822.0, 59058.0, 58400.0, 58603.0, 2369545.0], [1617696000000, 58610.0, 58989.0, 58362.0, 58587.0, 271731.0], [1617710400000, 58587.0, 59117.0, 57524.0, 57943.0, 900232.0], [1617724800000, 57917.0, 58315.0, 57850.0, 58280.0, 273645.0], [1617739200000, 58280.0, 58350.0, 57664.0, 58080.0, 294937.0], [1617753600000, 58080.0, 58250.0, 57300.0, 57975.0, 448514.0], [1617768000000, 57983.0, 58671.0, 57353.0, 57903.0, 706415.0], [1617782400000, 57906.0, 57995.0, 55833.0, 56379.0, 2059844.0], [1617796800000, 56370.0, 56987.0, 55653.0, 56498.0, 970339.0], [1617811200000, 56529.0, 56848.0, 55552.0, 56181.0, 994078.0], [1617825600000, 56188.0, 56642.0, 55807.0, 56019.0, 661793.0], [1617840000000, 56002.0, 56730.0, 55750.0, 56606.0, 657289.0], [1617854400000, 56572.0, 57357.0, 56560.0, 57067.0, 441781.0], [1617868800000, 57075.0, 57300.0, 56400.0, 56464.0, 496026.0], [1617883200000, 56448.0, 57980.0, 56394.0, 57783.0, 756373.0], [1617897600000, 57804.0, 58200.0, 57577.0, 57763.0, 1287929.0], [1617912000000, 57770.0, 58210.0, 57482.0, 58122.0, 963191.0], [1617926400000, 58124.0, 58463.0, 57825.0, 58030.0, 466713.0], [1617940800000, 58012.0, 58346.0, 57700.0, 58113.0, 443018.0], [1617955200000, 58107.0, 58931.0, 57725.0, 58549.0, 666772.0], [1617969600000, 58578.0, 58816.0, 58082.0, 58271.0, 1277171.0], [1617984000000, 58275.0, 58525.0, 57900.0, 58396.0, 581759.0], [1617998400000, 58397.0, 58623.0, 57925.0, 58150.0, 599723.0], [1618012800000, 58151.0, 59238.0, 57929.0, 59231.0, 905290.0], [1618027200000, 59234.0, 61701.0, 59234.0, 60651.0, 2092027.0], [1618041600000, 60651.0, 61079.0, 60574.0, 60685.0, 1009201.0], [1618056000000, 60699.0, 60911.0, 59941.0, 60316.0, 1430161.0], [1618070400000, 60301.0, 60603.0, 59334.0, 59580.0, 578246.0], [1618084800000, 59568.0, 59925.0, 58423.0, 59874.0, 880055.0], [1618099200000, 59855.0, 60802.0, 59708.0, 60375.0, 559648.0], [1618113600000, 60353.0, 60411.0, 59452.0, 59733.0, 831845.0], [1618128000000, 59732.0, 60224.0, 59500.0, 59788.0, 578226.0], [1618142400000, 59809.0, 59930.0, 59330.0, 59748.0, 325442.0], [1618156800000, 59737.0, 60314.0, 59461.0, 59753.0, 386792.0]]
    klines2 = [[1615305600000, 54219.0, 54379.0, 53661.0, 54129.0, 305719.0], [1615320000000, 54127.0, 54913.0, 53920.0, 54893.0, 957932.0], [1615334400000, 54893.0, 55825.0, 53200.0, 53494.0, 1590035.0], [1615348800000, 53538.0, 54445.0, 53090.0, 54223.0, 595907.0], [1615363200000, 54232.0, 55512.0, 54100.0, 54889.0, 396763.0], [1615377600000, 54899.0, 56527.0, 54852.0, 56344.0, 671089.0], [1615392000000, 56335.0, 57433.0, 56102.0, 56776.0, 827287.0], [1615406400000, 56798.0, 57320.0, 55604.0, 55930.0, 694332.0], [1615420800000, 55959.0, 56587.0, 55271.0, 56041.0, 511981.0], [1615435200000, 56026.0, 56262.0, 55082.0, 55100.0, 592893.0], [1615449600000, 55125.0, 56285.0, 54330.0, 56223.0, 566217.0], [1615464000000, 56249.0, 57289.0, 55794.0, 56346.0, 1240856.0], [1615478400000, 56348.0, 57763.0, 56303.0, 56829.0, 885852.0], [1615492800000, 56869.0, 58213.0, 56564.0, 57794.0, 894201.0], [1615507200000, 57812.0, 58111.0, 56700.0, 57173.0, 544966.0], [1615521600000, 57150.0, 57495.0, 56400.0, 56758.0, 416555.0], [1615536000000, 56754.0, 57154.0, 55859.0, 56468.0, 465627.0], [1615550400000, 56503.0, 57162.0, 55090.0, 56988.0, 1298401.0], [1615564800000, 56998.0, 57776.0, 56736.0, 56952.0, 828591.0], [1615579200000, 56954.0, 57548.0, 56300.0, 57322.0, 573885.0], [1615593600000, 57353.0, 57362.0, 56130.0, 56709.0, 350969.0], [1615608000000, 56707.0, 57473.0, 56292.0, 57425.0, 1391142.0], [1615622400000, 57424.0, 60334.0, 57138.0, 59910.0, 2432282.0], [1615636800000, 59918.0, 60499.0, 59291.0, 59719.0, 809250.0], [1615651200000, 59725.0, 60870.0, 59489.0, 60765.0, 888854.0], [1615665600000, 60768.0, 61910.0, 60699.0, 61249.0, 1474951.0], [1615680000000, 61250.0, 61742.0, 60792.0, 61356.0, 1177156.0], [1615694400000, 61352.0, 61517.0, 60534.0, 60565.0, 664503.0], [1615708800000, 60564.0, 61175.0, 59460.0, 60398.0, 1239456.0], [1615723200000, 60359.0, 60634.0, 59566.0, 59781.0, 313712.0], [1615737600000, 59781.0, 60463.0, 59379.0, 59996.0, 285756.0], [1615752000000, 59996.0, 60798.0, 58965.0, 58999.0, 1845054.0], [1615766400000, 58958.0, 60534.0, 58756.0, 60410.0, 707757.0], [1615780800000, 60431.0, 60708.0, 57336.0, 57881.0, 1497949.0], [1615795200000, 57880.0, 58434.0, 54400.0, 56151.0, 3009066.0], [1615809600000, 56143.0, 57286.0, 55090.0, 56231.0, 1658860.0], [1615824000000, 56233.0, 56692.0, 55500.0, 56585.0, 794653.0], [1615838400000, 56574.0, 56940.0, 55587.0, 55680.0, 511996.0], [1615852800000, 55651.0, 56101.0, 53337.0, 54323.0, 1409401.0], [1615867200000, 54324.0, 55494.0, 53676.0, 55272.0, 682230.0], [1615881600000, 55262.0, 56424.0, 55155.0, 55474.0, 342495.0], [1615896000000, 55508.0, 55951.0, 54701.0, 55881.0, 1025848.0], [1615910400000, 55881.0, 56130.0, 55011.0, 55778.0, 1364937.0], [1615924800000, 55763.0, 56932.0, 55734.0, 56907.0, 1032990.0], [1615939200000, 56913.0, 57198.0, 55450.0, 55515.0, 846115.0], [1615953600000, 55525.0, 56350.0, 55256.0, 55861.0, 516858.0], [1615968000000, 55860.0, 56102.0, 54448.0, 54841.0, 1039071.0], [1615982400000, 54865.0, 55452.0, 54177.0, 54983.0, 1388614.0], [1615996800000, 54978.0, 58179.0, 54798.0, 57853.0, 1448611.0], [1616011200000, 57866.0, 58965.0, 57586.0, 58883.0, 1540696.0], [1616025600000, 58884.0, 59536.0, 58655.0, 58778.0, 824648.0], [1616040000000, 58802.0, 59249.0, 58171.0, 58408.0, 926630.0], [1616054400000, 58398.0, 58721.0, 57950.0, 58218.0, 448501.0], [1616068800000, 58194.0, 59664.0, 57569.0, 59530.0, 1125850.0], [1616083200000, 59598.0, 60130.0, 57266.0, 57317.0, 1455113.0], [1616097600000, 57333.0, 58140.0, 57031.0, 57652.0, 1207199.0], [1616112000000, 57652.0, 57888.0, 56302.0, 57780.0, 537160.0], [1616126400000, 57800.0, 58495.0, 57606.0, 57810.0, 626190.0], [1616140800000, 57865.0, 58905.0, 57525.0, 58821.0, 439605.0], [1616155200000, 58850.0, 59268.0, 57978.0, 59014.0, 839858.0], [1616169600000, 59047.0, 59212.0, 58389.0, 58869.0, 1023873.0], [1616184000000, 58891.0, 59500.0, 58044.0, 58092.0, 1092950.0], [1616198400000, 58050.0, 58971.0, 57856.0, 58475.0, 561400.0], [1616212800000, 58475.0, 58651.0, 58034.0, 58473.0, 272265.0], [1616227200000, 58479.0, 59370.0, 58479.0, 59316.0, 221259.0], [1616241600000, 59352.0, 59948.0, 58638.0, 59266.0, 883732.0], [1616256000000, 59331.0, 59482.0, 58953.0, 59301.0, 267801.0], [1616270400000, 59312.0, 59403.0, 58050.0, 58145.0, 780577.0], [1616284800000, 58121.0, 58599.0, 57469.0, 57798.0, 591622.0], [1616299200000, 57765.0, 57811.0, 56710.0, 57061.0, 1363223.0], [1616313600000, 57001.0, 57387.0, 55470.0, 56257.0, 782822.0], [1616328000000, 56220.0, 57562.0, 55917.0, 57199.0, 1449883.0], [1616342400000, 57175.0, 57698.0, 56744.0, 57540.0, 835530.0], [1616356800000, 57550.0, 58166.0, 57238.0, 57410.0, 793689.0], [1616371200000, 57390.0, 57699.0, 56347.0, 57607.0, 931695.0], [1616385600000, 57633.0, 57926.0, 57358.0, 57636.0, 340922.0], [1616400000000, 57633.0, 58505.0, 57114.0, 57769.0, 339566.0], [1616414400000, 57781.0, 57822.0, 56601.0, 57094.0, 1188973.0], [1616428800000, 57104.0, 57240.0, 55526.0, 55582.0, 785383.0], [1616443200000, 55566.0, 56055.0, 53400.0, 54106.0, 1889210.0], [1616457600000, 54109.0, 55325.0, 53826.0, 54678.0, 905705.0], [1616472000000, 54688.0, 54803.0, 52989.0, 54218.0, 1316059.0], [1616486400000, 54218.0, 54850.0, 53008.0, 54249.0, 1077253.0], [1616500800000, 54287.0, 55498.0, 54287.0, 55243.0, 1366731.0], [1616515200000, 55251.0, 55833.0, 54877.0, 55050.0, 928829.0], [1616529600000, 55022.0, 55111.0, 54250.0, 54432.0, 786729.0], [1616544000000, 54409.0, 54828.0, 53601.0, 54442.0, 874511.0], [1616558400000, 54400.0, 55638.0, 53753.0, 55522.0, 1429530.0], [1616572800000, 55476.0, 56713.0, 55474.0, 56567.0, 1451850.0], [1616587200000, 56575.0, 57192.0, 56084.0, 56344.0, 765786.0], [1616601600000, 56406.0, 56472.0, 54732.0, 54807.0, 1250362.0], [1616616000000, 54784.0, 54784.0, 51714.0, 52307.0, 2090776.0], [1616630400000, 52304.0, 52827.0, 51520.0, 52140.0, 2282302.0], [1616644800000, 52141.0, 53229.0, 51935.0, 52276.0, 1427792.0], [1616659200000, 52286.0, 53136.0, 52102.0, 52200.0, 1501959.0], [1616673600000, 52184.0, 52369.0, 50510.0, 50994.0, 3254369.0], [1616688000000, 51013.0, 52580.0, 50600.0, 52196.0, 1825074.0], [1616702400000, 52219.0, 52732.0, 51260.0, 51351.0, 985713.0], [1616716800000, 51345.0, 52722.0, 51269.0, 52420.0, 1549119.0], [1616731200000, 52459.0, 53560.0, 52215.0, 53524.0, 1099256.0], [1616745600000, 53558.0, 53820.0, 52621.0, 52761.0, 1821044.0], [1616760000000, 52771.0, 53543.0, 52576.0, 53295.0, 1408975.0], [1616774400000, 53324.0, 54035.0, 52905.0, 53757.0, 1954470.0], [1616788800000, 53773.0, 55077.0, 53773.0, 55049.0, 2116912.0], [1616803200000, 55049.0, 55550.0, 54515.0, 54776.0, 1592307.0], [1616817600000, 54818.0, 55359.0, 54673.0, 54983.0, 817641.0], [1616832000000, 54974.0, 55162.0, 54329.0, 54467.0, 936485.0], [1616846400000, 54478.0, 55039.0, 54010.0, 54990.0, 1369094.0], [1616860800000, 54987.0, 56292.0, 54987.0, 55798.0, 1161177.0], [1616875200000, 55792.0, 56639.0, 55710.0, 55820.0, 1317500.0], [1616889600000, 55806.0, 56180.0, 55566.0, 56031.0, 1294648.0], [1616904000000, 56029.0, 56460.0, 55850.0, 56207.0, 238459.0], [1616918400000, 56208.0, 56562.0, 55700.0, 55822.0, 612525.0], [1616932800000, 55809.0, 56396.0, 55315.0, 56380.0, 1088961.0], [1616947200000, 56376.0, 56489.0, 54700.0, 55185.0, 1756935.0], [1616961600000, 55214.0, 55885.0, 54801.0, 55797.0, 1694041.0], [1616976000000, 55800.0, 55931.0, 55013.0, 55374.0, 1552450.0], [1616990400000, 55380.0, 56187.0, 54944.0, 55920.0, 1275576.0], [1617004800000, 55930.0, 58350.0, 55873.0, 57862.0, 1327142.0], [1617019200000, 57900.0, 58449.0, 57301.0, 57725.0, 1166521.0], [1617033600000, 57730.0, 58350.0, 57225.0, 57676.0, 789824.0], [1617048000000, 57699.0, 57950.0, 57138.0, 57689.0, 1176567.0], [1617062400000, 57688.0, 57798.0, 57193.0, 57266.0, 1029037.0], [1617076800000, 57261.0, 58336.0, 57153.0, 58167.0, 1808843.0], [1617091200000, 58168.0, 59427.0, 57762.0, 59286.0, 1822415.0], [1617105600000, 59296.0, 59463.0, 58622.0, 58651.0, 1021702.0], [1617120000000, 58650.0, 59229.0, 58600.0, 59131.0, 836234.0], [1617134400000, 59130.0, 59153.0, 58431.0, 58815.0, 1704417.0], [1617148800000, 58813.0, 59090.0, 58416.0, 58650.0, 944926.0], [1617163200000, 58659.0, 59939.0, 57332.0, 58199.0, 2058915.0], [1617177600000, 58284.0, 58359.0, 56856.0, 58101.0, 2530745.0], [1617192000000, 58101.0, 59494.0, 57765.0, 59367.0, 1888152.0], [1617206400000, 59343.0, 59719.0, 58465.0, 58671.0, 1927467.0], [1617220800000, 58689.0, 59426.0, 58415.0, 58875.0, 1315482.0], [1617235200000, 58875.0, 59400.0, 58857.0, 59200.0, 844829.0], [1617249600000, 59200.0, 59295.0, 58579.0, 58900.0, 1981415.0], [1617264000000, 58900.0, 59520.0, 58068.0, 58597.0, 1052067.0], [1617278400000, 58596.0, 59339.0, 58427.0, 59046.0, 1199370.0], [1617292800000, 59047.0, 59213.0, 58017.0, 58976.0, 1456603.0], [1617307200000, 58976.0, 59121.0, 58604.0, 58828.0, 1087958.0], [1617321600000, 58857.0, 60381.0, 58528.0, 59949.0, 1819809.0], [1617336000000, 59950.0, 60073.0, 59453.0, 59560.0, 1472870.0], [1617350400000, 59555.0, 59759.0, 59314.0, 59619.0, 1003762.0], [1617364800000, 59620.0, 59718.0, 59085.0, 59567.0, 1520980.0], [1617379200000, 59567.0, 59673.0, 58555.0, 58887.0, 606436.0], [1617393600000, 58890.0, 59303.0, 58580.0, 59069.0, 786042.0], [1617408000000, 59062.0, 59500.0, 59013.0, 59295.0, 596721.0], [1617422400000, 59286.0, 59655.0, 59265.0, 59403.0, 1167682.0], [1617436800000, 59428.0, 59890.0, 58851.0, 59353.0, 638400.0], [1617451200000, 59345.0, 59578.0, 58901.0, 58901.0, 1279487.0], [1617465600000, 58905.0, 59202.0, 57833.0, 58629.0, 1271374.0], [1617480000000, 58612.0, 58612.0, 56930.0, 57147.0, 1076625.0], [1617494400000, 57137.0, 57611.0, 56521.0, 57539.0, 1218697.0], [1617508800000, 57524.0, 57722.0, 57236.0, 57650.0, 622248.0], [1617523200000, 57692.0, 57800.0, 57183.0, 57302.0, 255981.0], [1617537600000, 57314.0, 58572.0, 57073.0, 57960.0, 1060653.0], [1617552000000, 57970.0, 58295.0, 57718.0, 57998.0, 606725.0], [1617566400000, 57998.0, 58333.0, 57900.0, 58242.0, 431293.0], [1617580800000, 58266.0, 58456.0, 57405.0, 57567.0, 358154.0], [1617595200000, 57567.0, 57675.0, 56842.0, 57332.0, 702245.0], [1617609600000, 57306.0, 57779.0, 56821.0, 57772.0, 265434.0], [1617624000000, 57779.0, 59339.0, 57779.0, 59052.0, 844655.0], [1617638400000, 59077.0, 59289.0, 58703.0, 59112.0, 873172.0], [1617652800000, 59106.0, 59247.0, 58618.0, 59247.0, 477498.0], [1617667200000, 59246.0, 59600.0, 58712.0, 58823.0, 897297.0], [1617681600000, 58822.0, 59058.0, 58400.0, 58603.0, 2369545.0], [1617696000000, 58610.0, 58989.0, 58362.0, 58587.0, 271731.0], [1617710400000, 58587.0, 59117.0, 57524.0, 57943.0, 900232.0], [1617724800000, 57917.0, 58315.0, 57850.0, 58280.0, 273645.0], [1617739200000, 58280.0, 58350.0, 57664.0, 58080.0, 294937.0], [1617753600000, 58080.0, 58250.0, 57300.0, 57975.0, 448514.0], [1617768000000, 57983.0, 58671.0, 57353.0, 57903.0, 706415.0], [1617782400000, 57906.0, 57995.0, 55833.0, 56379.0, 2059844.0], [1617796800000, 56370.0, 56987.0, 55653.0, 56498.0, 970339.0], [1617811200000, 56529.0, 56848.0, 55552.0, 56181.0, 994078.0], [1617825600000, 56188.0, 56642.0, 55807.0, 56019.0, 661793.0], [1617840000000, 56002.0, 56730.0, 55750.0, 56606.0, 657289.0], [1617854400000, 56572.0, 57357.0, 56560.0, 57067.0, 441781.0], [1617868800000, 57075.0, 57300.0, 56400.0, 56464.0, 496026.0], [1617883200000, 56448.0, 57980.0, 56394.0, 57783.0, 756373.0], [1617897600000, 57804.0, 58200.0, 57577.0, 57763.0, 1287929.0], [1617912000000, 57770.0, 58210.0, 57482.0, 58122.0, 963191.0], [1617926400000, 58124.0, 58463.0, 57825.0, 58030.0, 466713.0], [1617940800000, 58012.0, 58346.0, 57700.0, 58113.0, 443018.0], [1617955200000, 58107.0, 58931.0, 57725.0, 58549.0, 666772.0], [1617969600000, 58578.0, 58816.0, 58082.0, 58271.0, 1277171.0], [1617984000000, 58275.0, 58525.0, 57900.0, 58396.0, 581759.0], [1617998400000, 58397.0, 58623.0, 57925.0, 58150.0, 599723.0], [1618012800000, 58151.0, 59238.0, 57929.0, 59231.0, 905290.0], [1618027200000, 59234.0, 61701.0, 59234.0, 60651.0, 2092027.0], [1618041600000, 60651.0, 61079.0, 60574.0, 60685.0, 1009201.0], [1618056000000, 60699.0, 60911.0, 59941.0, 60316.0, 1430161.0], [1618070400000, 60301.0, 60603.0, 59334.0, 59580.0, 578246.0], [1618084800000, 59568.0, 59925.0, 58423.0, 59874.0, 880055.0], [1618099200000, 59855.0, 60802.0, 59708.0, 60375.0, 559648.0], [1618113600000, 60353.0, 60411.0, 59452.0, 59733.0, 831845.0], [1618128000000, 59732.0, 60224.0, 59500.0, 59788.0, 578226.0], [1618142400000, 59809.0, 59930.0, 59330.0, 59748.0, 325442.0], [1618156800000, 59737.0, 60314.0, 59461.0, 59753.0, 386792.0], [1618171200000, 59758.0, 60216.0, 59540.0, 60092.0, 1390353.0]]
    df1 = pd.DataFrame(klines1, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df2 = pd.DataFrame(klines2, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    tasks = {
        "default": {
            "pair": "BTC-USDT",
            "timeFrame": "4h",
            "strategyName": "OneEMA",
            "botName": "",
            "startAt": "2021-01-01_00:00:00",
            "endAt": "2021-09-01_00:00:00",
            "volume": 1,
            "initialCapital": 100000,
            "market": "spot",
            "optimization": False,
            "randomInputs": False,
            "numberOfInputs": 5
        },
        "To_Do": [{
            "pair": "BTC-USDT",
            "timeFrame": "4h",
            "strategyName": "OneEMA",
            "botName": "",
            "startAt": "2021-01-01_00:00:00",
            "endAt": "2021-09-01_00:00:00",
            "volume": 1,
            "initialCapital": 100000,
            "market": "spot",
            "optimization": False,
            "randomInputs": False,
            "numberOfInputs": 5
        }],
        "Done": [{
            "pair": "BTC-USDT",
            "timeFrame": "4h",
            "strategyName": "OneEMA",
            "botName": "",
            "startAt": "2021-01-01 00:00:00",
            "endAt": "2021-09-01 00:00:00",
            "volume": 1,
            "initialCapital": 100000,
            "market": "spot",
            "optimization": True,
            "randomInputs": False,
            "numberOfInputs": 5,
            "doneAt": "2022-05-09_13-25-53"
        }]
    }