<?php

$action=$_GET['action'];
switch($action){
    case 'getProductionData':
        getProductionData();
    break;
}

function getProductionData(){
    // $flag=$_GET['flag'];
    $page=$_GET['page'];
    $maxRowPerPage=$_GET['maxRowPerPage'];
    $_startRow=(string)($page*$maxRowPerPage);
    $_endRow=(string)(($page+1)*$maxRowPerPage);

    $currHour=date('H');
    if($currHour>=8&&$currHour<20){
    	$currDate=date('Y-m-d');
        $sql='select product,device,hourProduction,num0 as num1,num1 as num2,num2 as num3,num3 as num4,num4 as num5,num5 as num6,
        num6 as num7,num7 as num8,num8 as num9,num9 as num10,num10 as num11,num11 as num12
        from chajiProductionData  where date=\''.$currDate.'\' order by device asc limit '.$_startRow.','.$_endRow.';';
    }else{
	$currDate=date('Y-m-d',strtotime("-1 day"));
        $sql='select product,device,hourProduction,num12 as num1,num13 as num2,num14 as num3,num15 as num4,num16 as num5,num17 as num6,
        num18 as num7,num19 as num8,num20 as num9,num21 as num10,num22 as num11,num23 as num12
        from chajiProductionData  where date=\''.$currDate.'\' order by device asc limit '.$_startRow.','.$_endRow.' order by device;';
        //     $prevDate=date("Y-m-d",strtotime("-1 day"));
        //     $_sql1='select 1 from chajiProduction where date=\''.$prevDate.'\'';
            
        //     $sql='select a.device,a.product,a.num20 as num1,a.num21 as num2,a.num22 as num3,a.num23 as num4,b.num0 as num5,b.num1 as num6,
        //      b.num2 as num7,b.num3 as num8,b.num4 as num9,b.num5 as num10,b.num6 as num11,b.num7 as num12 from chajiProduction as a
        //      join(select device,product,num0,num1,num2,num3,num4,num4,num6,num7 date from chajiProduction) as b 
        //      on a.device=b.device and a.product=b.product where a.date=\''.$prevDate.'\' and b.date=\''.$currDate.'\';';
        // }else{
        //     $nextDate=date("Y-m-d",strtotime("+1 day"));
        //     $sql='select a.device,a.product,a.num20 as num1,a.num21 as num2,a.num22 as num3,a.num23 as num4,b.num0 as num5,b.num1 as num6,
        //      b.num2 as num7,b.num3 as num8,b.num4 as num9,b.num5 as num10,b.num6 as num11,b.num7 as num12 from chajiProduction as a
        //      join(select device,product,num0,num1,num2,num3,num4,num4,num6,num7 date from chajiProduction) as b 
        //      on a.device=b.device and a.product=b.product where a.date=\''.$currDate.'\' and b.date=\''.$nextDate.'\';';

        // $sql='select product,device,num8 as num1,num9 as num2,num10 as num3,num11 as num4,num12 as num5,num13 as num6,
        // num14 as num7,num15 as num8,num16 as num9,num17 as num10,num18 as num11,num19 as num12
        // from chajiProduction  where date=\''.$currDate.'\' limit '.$_startRow.','.$_endRow.';';
        // echo $sql;
        // exit();
        // $sql='select product,device,num20 as num1, num21 as num2, num22 as num3,num23 as num4'
    }

    // echo $sql;
    $_data=[];
    $result=query_sql($sql);
    while($row=$result->fetch_assoc()){
        $_data[]=$row;
    }
    echo json_encode($_data);
    exit();
}


//数据库查询
function query_sql($sql){
    $mysqli = new mysqli("127.0.0.1",'te','123456','robot');
    $query = $mysqli->query($sql);
    $mysqli->close();
    return $query;
}
?>
