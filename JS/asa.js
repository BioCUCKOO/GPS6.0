var fontsize = 14;
var fontfamily = 'Verdana, sans-serif';

var x_p = 60;			//M氨基酸位点坐标，起始坐标，其他坐标均是该坐标的相对坐标
var y_p = 260;			//M氨基酸位点坐标，起始坐标，其他坐标均是该坐标的相对坐标
var gridwidth = 100;		//y轴网格线宽度

var lengend_x_p = 60;
var lengend_y_p = y_p - 15 - gridwidth * 2 - 25;

var max_yoffset = 10;
var kinaseTreeFlag = false;

function drawAxis(var1,var2){
	var codes = var1;
	var gps = var2;
	
	//origin coordinate
	var center_x = x_p - fontsize / 2;
	var center_y = y_p - fontsize / 2 - 5;
	
	var xAxis_x_start = center_x;
	var xAxis_y_start = center_y;	

	//origin start
	var yAxis_x_start = center_x;
	var yAxis_y_start = center_y;	
	
	//draw xAxis
	for(var i = 0; i < codes.length; i++) {		
		var xAxis_x_end = xAxis_x_start + fontsize;
		var xAxis_y_end = xAxis_y_start;		
		$('canvas.mycanvas').drawLine({
		  layer: true,
		  strokeStyle: '#000',
		  strokeWidth: 1,
		  x1: xAxis_x_start, y1: xAxis_y_start,
		  x2: xAxis_x_end, y2: xAxis_y_end,
		  x3: xAxis_x_end, y3: xAxis_y_end - 3,
		});		
		xAxis_x_start = xAxis_x_end;
	}	
	//draw xAxis arrow -- (xaxis length = codes.length * fontsize + 30)
	//$('canvas.mycanvas').drawLine({
	//  layer: true,
	//  strokeStyle: '#000',
	//  strokeWidth: 1,
	//  rounded: true,
	//  endArrow: true,
	//  arrowRadius: 6,
	//  arrowAngle: 90,
	//  x1: xAxis_x_start, y1: xAxis_y_start,
	//  x2: xAxis_x_start + 30, y2: xAxis_y_start,	  
	//});
	
	//draw yAxis	
	var v = 0.5;	
	for(var i = 0; i < 2; i++) {
		var yAxis_x_end = yAxis_x_start;
		var yAxis_y_end = yAxis_y_start - gridwidth; //grid width:72
		$('canvas.mycanvas').drawLine({
		  layer: true,
		  strokeStyle: '#000',
		  strokeWidth: 1,
		  x1: yAxis_x_start, y1: yAxis_y_start,
		  x2: yAxis_x_end, y2: yAxis_y_end,
		  x3: yAxis_x_end - 3, y3: yAxis_y_end,
		});
		$('canvas.mycanvas').drawText({
		  layer: true,
	      fillStyle: '#000',
		  strokeStyle: '#25a',
		  strokeWidth: 0,
		  x: yAxis_x_end - 13 - 10, y: yAxis_y_end,
		  fontSize: 12,
		  fontFamily: fontfamily,
		  text: v + "",		  
		});		
		yAxis_y_start = yAxis_y_end;
		v += 0.5;
	}
	$('canvas.mycanvas').drawLine({
		 layer: true, strokeStyle: '#000', strokeWidth: 1, x1: center_x, y1: center_y, x2: center_x-5, y2: center_y
	});
	$('canvas.mycanvas').drawText({
		 layer: true, fillStyle: '#000', strokeStyle: '#25a', strokeWidth: 0, x: yAxis_x_end - 13 - 10, y: center_y, fontSize: 12, fontFamily: fontfamily, text: "0",
	});
	
	//draw yAxis arrow -- (yaxis length = 2 * gridwidth + 30)
	//$('canvas.mycanvas').drawLine({
	//  layer: true,
	//  strokeStyle: '#000',
	//  strokeWidth: 1,
	//  rounded: true,
	//  endArrow: true,
	//  arrowRadius: 6,
	//  arrowAngle: 90,
	//  x1: yAxis_x_start, y1: yAxis_y_start,
	//  x2: yAxis_x_start, y2: yAxis_y_start - 30,	  
	//});
	
	//draw xAxis name
	for(var i=0;i<codes.length;i++) {
	var color = '#000';
		if(gps[i] == 1){
			color = 'red';
		}
		$('canvas.mycanvas').drawText({
		  layer: true,
	      fillStyle: color,
		  strokeStyle: '#25a',
		  strokeWidth: 0,
		  x: x_p + fontsize * i, y: y_p,
		  fontSize: fontsize,
		  fontFamily: fontfamily,
		  text: codes[i]
		});	
	}
	
	//draw yAxis threshold line
	var threshold_x_start = x_p - fontsize / 2;
	var threshold_y_start = center_y - gridwidth * 2 * 0.25;
	var threshold_x_end = threshold_x_start + fontsize * codes.length + 30;
	var threshold_y_end = threshold_y_start;
	$('canvas.mycanvas').drawLine({
	  layer: true,
	  strokeStyle: '#FFB265',
	  strokeWidth: 1,
	  strokeDash: [5],
	  x1: threshold_x_start, y1: threshold_y_start,
	  x2: threshold_x_end, y2: threshold_y_end,	  
	});
	$('canvas.mycanvas').drawText({
	  layer: true,
	  fillStyle: 'grey',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: threshold_x_start - 13 - 10, y: threshold_y_start,
	  fontSize: 12,
	  fontFamily: fontfamily,
	  text: "0.25"
	});
	//
	//
	threshold_y_start = center_y - gridwidth * 2 * 0.5;
	$('canvas.mycanvas').drawLine({
	  layer: true,
	  strokeStyle: '#B2D3EE',
	  strokeWidth: 1,
	  strokeDash: [5],
	  x1: threshold_x_start, y1: threshold_y_start,
	  x2: threshold_x_end, y2: threshold_y_start,	  
	});	
}

function drawAsa(var1, var2, var3, var4, var5, var6){
	var codes = var1;
	var values = var2;
	var linecolor = var3;
	var linecolorlight = var4;
	var title = var5;
	var index = var6;
	var positionValue = "";
	//draw line	
	for(var i=0;i < codes.length - 1;i++) {
		var value_x_start = x_p + fontsize * i;
		var value_y_start = y_p - 15 - gridwidth * 2 * values[i];
		var value_x_end = x_p + fontsize * (i + 1);
		var value_y_end = y_p - 15 - gridwidth * 2 * values[i + 1];		
		var k = values[i + 1];
		var c = codes[i + 1];
		positionValue = positionValue+value_x_end+"_"+value_y_end+":"+k+":"+c+"@";
		$('canvas.mycanvas').drawLine({
		  layer: true,		  
		  strokeStyle: linecolor,
		  strokeWidth: 2,
		  x1: value_x_start, y1: value_y_start,
		  x2: value_x_end, y2: value_y_end,		  
		});
		$('canvas.mycanvas').drawRect({
		  layer: true,			  	 
		  fillStyle: 'white',
		  opacity: 0,
		  strokeStyle: linecolor,
		  strokeWidth: 0,
		  x: value_x_end, y: value_y_end,
		  width: fontsize,
		  height: 100,
		  mouseover: function(layer) {
			$('canvas.mycanvas').drawEllipse({
				layer: true,
				groups: ['myPanel'],
				fillStyle: linecolor,				
				strokeStyle: linecolorlight,
				strokeWidth: 4,
				x: layer.x, y: layer.y,
				width: 16, height: 16
			});
			panel(layer.x,layer.y,"Value",positionValue, linecolor);			  
		  },
		  mouseout: function() {			  
			$('canvas.mycanvas').removeLayerGroup( 'myPanel' );
		  },		  
		});
		if(index == 0){
			$('canvas.mycanvas').drawEllipse({
			  layer: true,
			  fillStyle: linecolor,
			  x: value_x_end, y: value_y_end,
			  width: 7, height: 7,
			  mouseover: function(layer) {
				$('canvas.mycanvas').drawEllipse({
					layer: true,
					groups: ['myPanel'],
					fillStyle: linecolor,				
					strokeStyle: linecolorlight,
					strokeWidth: 4,
					x: layer.x, y: layer.y,
					width: 16, height: 16
				});
				panel(layer.x,layer.y,"Value",positionValue, linecolor);			  
			  },
			  mouseout: function() {			  
				$('canvas.mycanvas').removeLayerGroup( 'myPanel' );
			  },
			});
		}		
		if(index == 1){
			$('canvas.mycanvas').drawPolygon({
			  layer: true,
			  fillStyle: linecolor,
			  x: value_x_end, y: value_y_end,
			  radius: 5,
			  sides: 3,
			  mouseover: function(layer) {
				$('canvas.mycanvas').drawEllipse({
					layer: true,
					groups: ['myPanel'],
					fillStyle: linecolor,				
					strokeStyle: linecolorlight,
					strokeWidth: 4,
					x: layer.x, y: layer.y,
					width: 16, height: 16
				});
				panel(layer.x,layer.y,"Value",positionValue, linecolor);			  
			  },
			  mouseout: function() {			  
				$('canvas.mycanvas').removeLayerGroup( 'myPanel' );
			  },
			});
		}		
	}	
	
	//draw lenged
	var text = var5;
	var lengend_line_x_end = lengend_x_p + 25;
	var lengend_line_y_end = lengend_y_p;
	$('canvas.mycanvas').drawLine({
	  layer: true,
	  strokeStyle: linecolor,
	  strokeWidth: 1,
	  x1: lengend_x_p, y1: lengend_y_p + fontsize / 2,
	  x2: lengend_line_x_end, y2: lengend_line_y_end + fontsize / 2,
	  fromCenter: false
	});
	var lengend_text_x = lengend_line_x_end + 3;
	var lengend_text_y = lengend_y_p;
	$('canvas.mycanvas').drawText({
	  layer: true,
	  fillStyle: '#000',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: lengend_text_x, y: lengend_text_y,
	  fontSize: fontsize - 3,
	  fontFamily: fontfamily,
	  text: text,
	  fromCenter: false
	});	
	lengend_y_p = lengend_y_p + fontsize;	
}
function drawTitle(){
	//draw Title
	var text_x = x_p;
	var text_y = lengend_y_p - fontsize - 35;
	$('canvas.mycanvas').drawText({
	  layer: true,
	  fillStyle: 'black',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: x_p - fontsize / 2, y: text_y,
	  fontSize: fontsize + 5,
	  fontFamily: fontfamily,
	  text: "Predicted surface accessibility and disordered region",	
	  fromCenter: false,
	});
}

function drawSecondStructure(var1,var2,var3){
	var name= new Array("α-helix","Coil","β-strand");
	var codes = var1;
	var structure = var2;
	var gps = var3;
	var deep = y_p + 70;
	//draw disorder lengend
	var text_x = x_p;
	var text_y = deep - 40;
	$('canvas.mycanvas').drawText({
	  layer: true,
	  fillStyle: 'black',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: x_p - fontsize / 2, y: text_y,
	  fontSize: fontsize + 5,
	  //fontFamily: 'Arial',
	  fontFamily: fontfamily,
	  //text: "Second Structure: (  :Alpha-helix,   :Coil,   :Beta-strand)",
	  text: "Second structure: (   α-helix,     coil,     β-strand)",
	  fromCenter: false,
	});
	$('canvas.mycanvas').drawImage({
	  layer: true,
	  source: 'webcomp/img/h_white.png',
	  x: x_p - fontsize / 2 + 190, y: text_y,
	  width: fontsize,
	  height: fontsize + 8,
	  fromCenter: false,
	});
	$('canvas.mycanvas').drawLine({
	  layer: true,
	  strokeStyle: '#25a',
	  strokeWidth: 4,
	  x1: x_p - fontsize / 2 + 293, y1: text_y + 10,
	  x2: x_p - fontsize / 2 + 293 + 16, y2: text_y + 10,
	  fromCenter: false,
	});
	$('canvas.mycanvas').drawImage({
	  layer: true,
	  source: 'webcomp/img/arr.png',
	  x: x_p - fontsize / 2 + 363, y: text_y - 3,
	  width: fontsize+3,
	  height: fontsize + 14,
	  fromCenter: false,		  
	});	
	//draw protein chain
	$('canvas.mycanvas').drawLine({
	  layer: true,
	  strokeStyle: '#25a',
	  strokeWidth: 4,
	  x1: x_p, y1: deep,
	  x2: x_p + fontsize * (structure.length - 1), y2: deep,
	});
	
	var E_x_start = new Array();
	var E_x_end = new Array();
	var E_x_index = new Array();
	var xoffset = 10;
	var yoffset = 10;
	var previousIndex = 0;
	var nIndex = 1;	
	for(var i=0;i<structure.length;i++) {
		var color = "blue";
		if(structure[i] == 'E'){
			color = "red";
			E_x_index.push(i);
		}else if(structure[i] == 'C'){
			color = "green";			
		}else{
			$('canvas.mycanvas').drawImage({
			  layer: true,
			  source: 'webcomp/img/h_white.png',
			  x: x_p + fontsize * i, y: deep,
			  width: fontsize,
			  height: fontsize + 8,			  
			});
		}
		if(gps[i] == 1){
			if(i>0){
				var current_x_position = x_p + fontsize * i;
				var previous_x_position = x_p + fontsize * previousIndex;
				var nIndexString = nIndex.toString() + "K";
				//alert(nIndexString+" "+nIndexString.length);
				if((current_x_position - previous_x_position) < (nIndexString.length * fontsize)){
					xoffset = xoffset - 2;
					yoffset = yoffset + fontsize / 2;
				}else{
					var xoffset = 10;
					var yoffset = 10;
				}				
			}
			if(max_yoffset < yoffset){
				max_yoffset = yoffset;
			}
			$('canvas.mycanvas').drawLine({
			  layer: true,
			  index: 0,
			  strokeStyle: 'black',
			  strokeWidth: 1,
			  x1: x_p + fontsize * i, y1: deep + 2,
			  x2: x_p + fontsize * i - xoffset, y2: deep + 2 + yoffset,
			  x3: x_p + fontsize * i - xoffset, y3: deep + 2 + yoffset + yoffset,
			});
			$('canvas.mycanvas').drawText({
				layer: true,
				fillStyle: 'red',				
				x: x_p + fontsize * i - xoffset, y: deep + yoffset + yoffset + fontsize / 2,
				fontSize: fontsize,
				fontFamily: fontfamily,
				text: codes[i] + ( i + 1)
			});
			previousIndex = i;
		}
		nIndex++;
	}
	E_x_start.push(E_x_index[0]);
	for(var i=0;i<E_x_index.length - 1;i++) {
		var n = E_x_index[i+1] - E_x_index[i];
		if(n != 1){
			E_x_end.push(E_x_index[i]);
			E_x_start.push(E_x_index[i+1]);
		}
	}
	E_x_end.push(E_x_index[E_x_index.length-1]);
	for(var i=0;i<E_x_start.length;i++) {			
		for(var j = E_x_start[i];j<E_x_end[i];j++){
			$('canvas.mycanvas').drawImage({
			  layer: true,
			  source: 'webcomp/img/block.png',
			  x: x_p + fontsize * j, y: deep,
			  width: fontsize,
			  height: fontsize,
			});
		}
		$('canvas.mycanvas').drawImage({
		  layer: true,
		  source: 'webcomp/img/arr.png',
		  x: x_p + fontsize * E_x_end[i], y: deep,
		  width: fontsize,
		  height: fontsize + 14,			  
		});	
	}
}

function drawDisorder(var1){
	var codes = var1;
	var deep = y_p + 140;	
	//draw disorder lengend
	var text_x = x_p;
	var text_y = deep - 40;
	$('canvas.mycanvas').drawText({
	  layer: true,
	  fillStyle: '#9000FF',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: text_x - fontsize / 2, y: text_y,
	  fontSize: fontsize + 5,
	  fontFamily: fontfamily,
	  text: "Disorder region: (*)",	
	  fromCenter: false,
	});
	//draw disorder
	for(var i=0;i<codes.length;i++) {
		var v = codes[i];
		if(v == 'D'){
			v = "*";
		}
		if(v == 'O'){
			v = "-";
		}
		$('canvas.mycanvas').drawText({
		  layer: true,
	      fillStyle: '#9000FF',
		  strokeStyle: '#25a',
		  strokeWidth: 0,
		  x: x_p + fontsize * i, y: deep,
		  fontSize: fontsize,
		  fontFamily: 'Verdana, sans-serif',
		  text: v
		});	
	}
}

function drawNMCPsite(var1,var2){
	var codes = var1;
	var gps = var2;	
	var deep = y_p + 180;
	var k = new Array("AGC/GRK/GRK","AGC/GRK/GRK/GRK-1","AGC/PKC/Alpha/PKCg","AGC/RSK/RSK/RSK2","CK1/CK1/CK1e");
	var text_x = x_p;
	var text_y = deep - 40;
	$('canvas.mycanvas').drawText({
	  layer: true,
	  fillStyle: 'black',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: text_x - fontsize / 2, y: text_y,
	  fontSize: fontsize + 5,
	  fontFamily: fontfamily,
	  text: "Predicted Site:",	
	  fromCenter: false,
	});
	//draw N-terminal, Middle and C-terminal && P-site
	var len = codes.length;
	var step = Math.floor(len/3);
	var tag1 = step;
	var tag2 = step * 2;
	var tag3 = len;
	
	for(var i=0;i<codes.length;i++) {
		var color = "";
		if(i <= tag1){
			color = "#D8D800";
		}else if(i <= tag2 && i > tag1){
			color = "#C0EBCE";
		}else{
			color = "#8AC9EA";
		}		
		$('canvas.mycanvas').drawRect({
		  layer: true,
	      fillStyle: color,
		  x: x_p + fontsize * i, y: deep,
		  width: fontsize,
		  height: fontsize
		});
		if(gps[i] == 1){
			$('canvas.mycanvas').drawText({
			  layer: true,			  
			  fillStyle: 'red',
			  strokeStyle: '#25a',
			  strokeWidth: 0,
			  x: x_p + fontsize * i, y: deep,
			  fontSize: fontsize,
			  fontFamily: fontfamily,
			  text: codes[i],
			  mouseover: function() {
				$("canvas.mycanvas").css({cursor: "pointer"});
			  },
			  mouseout: function() {
				$("canvas.mycanvas").css({cursor: "default"});
			  },
			  click: function(layer) {
			  // Click a star to spin it
				//kinaseTree(layer.x,layer.y + 10,k);
			  }
			});			
		}else{
			$('canvas.mycanvas').drawText({
			  layer: true,
			  fillStyle: 'black',
			  strokeStyle: '#25a',
			  strokeWidth: 0,
			  x: x_p + fontsize * i, y: deep,
			  fontSize: fontsize,
			  fontFamily: fontfamily,
			  text: codes[i],			  
			});
		}
					
	}
}

function panel(var1,var2,var3,var4,var5){
	var start_x = var1;
	var start_y = var2;
	var type = var3;		
	var valueStr = var4;
	var panelcolor = var5;		
	//var color = var5;
	var regstr = start_x+"_"+start_y+":"+"(0\\.\\d+)"+":"+"(\\w)";
	var re =new RegExp(regstr);
	re.test(valueStr);
	var textValue = RegExp.$1;
	var textCode = RegExp.$2;
	//parameters
	var radius = 4;
	var panelWidth = 140;
	var panelHeight = 60;
	var distance_Polygon_rect = 13;		
	$('canvas.mycanvas').drawPolygon({
	  layer: true,
	  groups: ['myPanel'],
	  fillStyle: panelcolor,
	  strokeStyle: panelcolor,
	  strokeWidth: 2,
	  x: start_x, y: start_y - distance_Polygon_rect,
	  radius: 4,
	  sides: 3,
	  rotate: 180
	});
	$('canvas.mycanvas').drawRect({
	  layer: true,
	  groups: ['myPanel'],
	  fillStyle: 'white',
	  opacity: 0.8,
	  strokeStyle: panelcolor,
	  strokeWidth: 1,
	  x: start_x, y: start_y - distance_Polygon_rect - radius/2 - panelHeight/2,
	  width: panelWidth,
	  height: panelHeight,
	  cornerRadius: 8
	});
	  index = (start_x-46)/14
	$('canvas.mycanvas').drawText({
	  layer: true,
	  groups: ['myPanel'],
	  fillStyle: '#000000',
	  strokeStyle: '#000000',
	  strokeWidth: 0,
	  x: start_x - panelWidth/2 + 2 + 10, y: start_y - distance_Polygon_rect - radius/2 - panelHeight + 6,
	  fontSize: fontsize - 5,
	  fontFamily: fontfamily,
	  text: textCode + index,
	  fromCenter: false,
	});
	$('canvas.mycanvas').drawEllipse({
	  layer: true,
	  groups: ['myPanel'],
	  fillStyle: panelcolor,
	  x: start_x - panelWidth/2 + 2 + 10 + 5, y: start_y - distance_Polygon_rect - radius/2 - panelHeight + 6 + fontsize + 7,
	  width: 7, height: 7,	 
	});
	$('canvas.mycanvas').drawText({
	  layer: true,
	  groups: ['myPanel'],
	  fillStyle: '#000000',
	  strokeStyle: '#000000',
	  strokeWidth: 0,
	  x: start_x - panelWidth/2 + 2 + 10 + 15, y: start_y - distance_Polygon_rect - radius/2 - panelHeight + 6 + fontsize,
	  fontSize: fontsize - 5,
	  fontFamily: fontfamily,
	  text: type + ":  " +textValue,
	  fromCenter: false,
	});	
	$('canvas.mycanvas').drawLayers('myPanel');
}

function kinaseTree(var1,var2,var3){
	if(kinaseTreeFlag == true){
		$('canvas.mycanvas').removeLayerGroup( 'myBoxes' );
		$('canvas.mycanvas').drawLayers('myBoxes');
	}
	var start_x = var1;
	var start_y = var2;
	var kinases = var3;
	for(var i=0;i<kinases.length;i++) {
		var end_x = start_x;
		var end_y = start_y + fontsize;
		$('canvas.mycanvas').drawLine({
		  layer: true,		  
		  groups: ['myBoxes'],
		  strokeStyle: '#0088FF',
		  strokeWidth: 1,
		  x1: start_x, y1: start_y,
		  x2: end_x, y2: end_y,		  
		  x3: end_x + 4, y3: end_y,		  
		});
		$('canvas.mycanvas').drawText({
		  layer: true,		  
		  groups: ['myBoxes'],
	      fillStyle: '#0088FF',
		  strokeStyle: '#25a',
		  strokeWidth: 0,
		  x: end_x + 8, y: end_y - fontsize / 2,
		  fontSize: fontsize - 2,
		  fontFamily: fontfamily,
		  text: kinases[i],
		  fromCenter: false,
		});	
		start_x = end_x;
		start_y = end_y;
	}
	kinaseTreeFlag = true;
}

function getwidth(codes){
	var width = 130 + codes.length * fontsize;
	return width;
}

//draw tj chart
//draw STY distribution
function drawPieChart (var1, var2, var3,var4){
	var s_num = parseInt(var1);
	var t_num = parseInt(var2);
	var y_num = parseInt(var3);

	//parameters build-in
	var radius = 100;
	var rightoffset = var4;
	
	//origin coordinate
	var center_x = x_p + rightoffset;
	var center_y = 50 + radius;
	//alert(center_x);
	
	//calculate the angles
	var p1 = s_num/(s_num + t_num + y_num) * 360;
	var p2 = t_num/(s_num + t_num + y_num) * 360;
	var p3 = y_num/(s_num + t_num + y_num) * 360;
	//
	var x1 = center_x + Math.cos((135 - p1/2)*Math.PI*2/360) * radius/2;
	var y1 = center_y - Math.sin((135 - p1/2)*Math.PI*2/360)* radius/2;
	var percent1 = Math.round(p1/360 * 100);
	//
	var x2 = center_x + Math.cos((-135 + p1 + p2/2)*Math.PI*2/360)* radius / 2;
	var y2 = center_y + Math.sin((-135 + p1 + p2/2)*Math.PI*2/360) * radius / 2;
	var percent2 = Math.round(p2/360 * 100);
	//
	var x3 = center_x - Math.cos((315 - p1 - p2 - p3/2)*Math.PI*2/360)* radius / 2;
	var y3 = center_y + Math.sin((315 - p1 - p2 - p3/2)*Math.PI*2/360) * radius / 2;
	var percent3 = Math.round(p3/360 * 100);
	//
	if(p1 != 0 && p2 == 0 && p3 ==0){
		$('canvas.tj')
		.drawEllipse({
			layer: true,
			name: 'red-slice',			
			fillStyle: '#c33',
			x: center_x, y: center_y,
			width: radius * 2, height: radius * 2
		})
		.drawText({
			layer: true,
			name: 'red-label',
			fillStyle: '#fff',
			x: center_x, y: center_y,
			fontFamily: fontfamily,
			fontSize: fontsize,
			text: 'S: ' + percent1 + "%"
		})
	}else if(p1 == 0 && p2 != 0 && p3 ==0){
		$('canvas.tj')
		.drawEllipse({
			layer: true,
			name: 'green-slice',			
			fillStyle: '#6c0',
			x: center_x, y: center_y,
			width: radius * 2, height: radius * 2
		})
		.drawText({
			layer: true,
			name: 'green-label',
			fillStyle: '#fff',
			x: center_x, y: center_y,
			fontFamily: fontfamily,
			fontSize: fontsize,
			text: 'T: ' + percent2 + "%"
		})
	}else if(p1 == 0 && p2 == 0 && p3 !=0){
		$('canvas.tj')
		.drawEllipse({
			layer: true,
			name: 'blue-slice',			
			fillStyle: '#36c',
			x: center_x, y: center_y,
			width: radius * 2, height: radius * 2
		})
		.drawText({
			layer: true,
			name: 'blue-label',
			fillStyle: '#fff',
			x: center_x, y: center_y,
			fontFamily: fontfamily,
			fontSize: fontsize,
			text: 'Y: ' + percent3 + "%"
		})
	}else{
		$('canvas.tj').drawSlice({
			layer: true,
			name: 'red-slice',
			groups: ['chart', 'slices'],
			fillStyle: '#c33',
			x: center_x, y: center_y,
			start: -45, end: p1 - 45,
			radius: radius,
			spread: 1 / 40
		});
		$('canvas.tj').drawSlice({
			layer: true,
			name: 'green-slice',
			groups: ['chart', 'slices'],
			fillStyle: '#6c0',
			x: center_x, y: center_y,
			start: p1 - 45, end: p2 + p1 -45,
			radius: radius,
			spread: 1 / 40
		});
		$('canvas.tj').drawSlice({
			layer: true,
			name: 'blue-slice',
			groups: ['chart', 'slices'],
			fillStyle: '#36c',
			x: center_x, y: center_y,
			start: p2 + p1 -45, end: -45,
			radius: radius,
			spread: 1 / 40
		});
		if(p1 != 0){
			$('canvas.tj').drawText({
				layer: true,
				name: 'red-label',
				groups: ['chart', 'labels'],
				fillStyle: '#fff',
				x: x1, y: y1,
				fontFamily: fontfamily,
				fontSize: fontsize,
				text: 'S: ' + percent1 + "%"
			});
		}
		if(p2 != 0){
			$('canvas.tj').drawText({
				layer: true,
				name: 'green-label',
				groups: ['chart', 'labels'],
				fillStyle: '#fff',
				x: x2, y: y2,
				fontFamily: fontfamily,
				fontSize: fontsize,
				text: 'T: ' + percent2 + "%"
			});
		}
		if(p3 != 0){	
			$('canvas.tj').drawText({
				layer: true,
				name: 'blue-label',
				groups: ['chart', 'labels'],
				fillStyle: '#fff',
				x: x3, y: y3,
				fontFamily: fontfamily,
				fontSize: fontsize,
				text: 'Y: ' + percent3 + "%"
			});
		}
	}
	//draw legend
	var lengend_x_start = center_x;
	var lengend_y_start = center_y - radius - 20;
	$('canvas.tj').drawText({
	  layer: true,		  		 
	  fillStyle: 'black',
	  x: lengend_x_start, y: lengend_y_start,
	  fontSize: 15,
	  fontFamily: fontfamily,
	  text: 'S/T/Y distribution',	  
	});
}

function drawPieChart2 (var1, var2, var3,var4){
	//****************************************************************************************************//
	//**	var kinaseGroup = new Array("AGC","CAMK","CMGC","CK1","RGC","TK","TKL","Other");			**//
	//**	var siteNumber = new Array(30,40,50,20,60,80,10,40);										**//
	//**	drawPieChart2(kinaseGroup,siteNumber,"Distribution of S/T/Y",400);							**//
	//****************************************************************************************************//
	var names = var1;
	var numbers = var2;
	var legend = var3;
	var rightoffset = var4;
	
	//parameters build-in
	var radius = 100;
	var center_x = x_p + rightoffset;
	var center_y = 50 + radius;
	var colors = ['#A5E018','#A52DD4','#11E0B1','#F77617','#82B15C','#E110B5','#CBFA58','#3F124A','#1E7A43'];//the front 8 build-in colors
	//parseInt
	for(var i = 0;i < numbers.length;i++){
		numbers[i] = parseInt(numbers[i]);		
	}
	// draw pie chart
	var zero = 0;
	var index = 0;
	var total = 0;	
	for(var i = 0;i < numbers.length;i++){
		total = total + numbers[i];	
		if(numbers[i] != 0){
			zero++;
			index = i;
		}		
	}
	//alert(zero+":" + index);
	if(zero == 1){
		$('canvas.tj')
		.drawEllipse({
			layer: true,
			fillStyle: colors[index],
			x: center_x, y: center_y,
			width: radius * 2, height: radius * 2
		})
		.drawText({
			layer: true,			
			fillStyle: '#fff',
			x: center_x, y: center_y,
			fontFamily: fontfamily,
			fontSize: fontsize-1,
			text: names[index] + "\n" + '100' + "%"
		})
	}else{
		var start = -90;
		var end = -90;	
		for(var i = 0;i < numbers.length;i++){
			var angle = numbers[i] / total * 360;		
			if(i == 0){
				end  = start + angle;			
			}else if(i == numbers.length - 1){
				start = end;
				end = -90;			
			}else{
				start = end;
				end = start + angle;
			}
			var random_color = "";
			if(i < colors.length){
				random_color = colors[i];
			}else{
				random_color = "#" + randomColor();
				// while(colors.indexOf(random_color) == 0){
					// random_color = "#" + randomColor();
				// }
			}
			if(angle == 0){
				end = start;
			}
			$('canvas.tj').drawSlice({
				layer: true,
				index: 0,
				name: names[i],
				groups: ['chart', 'slices'],
				fillStyle: random_color,
				x: center_x, y: center_y,
				start: start, end: end,
				radius: radius,
				spread: 1 / 40
			})		
		}
		// draw pie chart percent text
		start = -90;
		end = -90;
		var x = center_x;
		var y = center_y;
		for(var i = 0;i < numbers.length;i++){
			var angle = numbers[i] / total * 360;
			if(angle != 0){
				if(i == 0){
					end  = start + angle;
					x = center_x - Math.cos((angle/2) * Math.PI * 2/360) * radius * 2/3;
					y = center_y - Math.sin((angle/2) * Math.PI * 2/360) * radius * 2/3;
				}else if(i == numbers.length - 1){
					start = end;
					end = -90;
					x = center_x + Math.cos((90- angle/2 - start) * Math.PI * 2/360) * radius * 2/3;
					y = center_y - Math.sin((90- angle/2 - start) * Math.PI * 2/360) * radius * 2/3;
				}else{
					start = end;
					end = start + angle;			
					x = center_x + Math.cos((90- angle/2 - start) * Math.PI * 2/360) * radius * 2/3;
					y = center_y - Math.sin((90- angle/2 - start) * Math.PI * 2/360) * radius * 2/3;
				}
				var percent = Math.round(angle/360 * 100);
				$('canvas.tj').drawText({
					layer: true,			
					fillStyle: '#000000',
					x: x, y: y,
					fontFamily: fontfamily,
					//fontSize: fontsize - 10,
					fontSize: fontsize-1,
					text: names[i] + "\n" + percent + "%"
				})
			}		
		}
	}
	//draw legend
	var lengend_x_start = center_x;
	var lengend_y_start = center_y - radius - 20;
	$('canvas.tj').drawText({
	  layer: true,		  		 
	  fillStyle: 'black',
	  x: lengend_x_start, y: lengend_y_start,
	  fontSize: 15,
	  fontFamily: fontfamily,
	  text: legend,	  
	});
}

function randomColor( ) {  
	var rand = Math.floor(Math.random( ) * 0xFFFFFF).toString(16);  
	if(rand.length == 6){  
		return rand;  
	}else{  
		return randomColor();  
	}
}
function drawTjAxis(var1,var2,var3,var4){
	//********************************************************************************//
	//**	var structureName = new Array("Alpha-Helix","Coil","Beat-strand");		**//
	//**	var structureValue = [[8,9,7],[5,7,10],[3,5,4]];						**//
	//**	drawTjAxis(structureName,structureValue,"Distribution of S/T/Y",600);	**//
	//********************************************************************************//
	var names = var1;
	var values = var2;
	var legend = var3;
	var rightoffset = var4;
	
	//parameters build-in
	var deep = 250;	
	var x_length = 260;	//x-axis length width
	var y_length = 180;	//y-axis length width
	var barwidth = 18;	//bar width
	var y_scale = 2;	//y-axis scale number
	
	//origin coordinate
	var origin_x = x_p + rightoffset;	// refer the origin coordinate is ok
	var origin_y = deep;				// refer the origin coordinate is ok
		
	//x axis end 
	var xAxis_x_end = origin_x + x_length;
	var xAxis_y_end = origin_y;	
	//y axis end 
	var yAxis_x_end = origin_x;
	var yAxis_y_end = origin_y - y_length;	
	
	//draw xAxis
	$('canvas.tj').drawLine({
	  layer: true,
	  strokeStyle: '#000',
	  strokeWidth: 2,
	  rounded: true,
	  endArrow: false,
	  arrowRadius: 6,
	  arrowAngle: 90,
	  x1: origin_x, y1: origin_y,
	  x2: xAxis_x_end, y2: xAxis_y_end,
	});
	
	
	//draw yAxis
	$('canvas.tj').drawLine({
	  layer: true,
	  strokeStyle: '#000',
	  strokeWidth: 2,
	  rounded: true,
	  endArrow: false,
	  arrowRadius: 6,
	  arrowAngle: 90,
	  x1: origin_x, y1: origin_y,
	  x2: yAxis_x_end, y2: yAxis_y_end,
	});	
	//draw bar	
	var x_step = x_length / values.length;
	var color = new Array("#c33","#6c0","#36c");
	var max = 0;	
	for(var i =0; i < values.length;i++){
		var arr = values[i];
		for(var j =0; j < arr.length;j++){
			arr[j] = parseInt(arr[j]);
			if(arr[j] > max){				
				max = arr[j];
			}
		}
	}
	$('canvas.tj').drawText({
	  layer: true, fillStyle: '#000', x: origin_x-20 , y: origin_y,//text downoffset
	  fontSize: 12,
	  fontFamily: fontfamily,
	  text: "0.0",
	});
	$('canvas.tj').drawLine({
		 layer: true, strokeStyle: '#000', strokeWidth: 2, x1: origin_x, y1: origin_y,x2: origin_x-6, y2: origin_y,
	});
	
	//alert(max);
	for(var i =0; i < values.length;i++){
		var arr = values[i];		
		var position_x = origin_x + x_step * (i + 1) - barwidth * arr.length / 2-30;		
		for(var j =0; j < arr.length;j++){
			var Coloum_x_start = position_x + j * barwidth;
			var Coloum_y_start = origin_y - (arr[j] / max) * y_length / 2;
			var height = (arr[j] / max) * y_length;			
			$('canvas.tj').drawRect({
			  layer: true,
			  fillStyle: color[j],			  
			  x: Coloum_x_start, y: Coloum_y_start,
			  width: barwidth,
			  height: height,
			});
		}
		//draw x axis name
		$('canvas.tj').drawText({
		  layer: true,		  		 
	      fillStyle: '#0088FF',
		  x: position_x + barwidth * arr.length / 2 - 15, y: origin_y + 12,//text downoffset
		  fontSize: fontsize,
		  fontFamily: fontfamily,
		  text: names[i],		  
		});	
		$('canvas.tj').drawLine({
			layer: true, strokeStyle: '#000', strokeWidth: 2, x1: origin_x + x_length/values.length*(i+1), y1: origin_y,x2: origin_x + x_length/values.length*(i+1), y2: origin_y+10,
		});
	}
	//draw y-scale rule text	
	var y_step = y_length % y_scale;
	if(y_step == 0){
		y_step = y_length / y_scale
	}else{
		y_step = (y_length - y_step) / y_scale;
	}
	for(var i = 1;i <= y_scale;i++){
		var line_start_x = origin_x - 4;
		var line_start_y = origin_y - i * y_step;
		var line_end_x = xAxis_x_end;
		var line_end_y = line_start_y;
		$('canvas.tj').drawLine({
		  layer: true,
		  strokeStyle: '#000',
		  strokeWidth: 1,
		  strokeDash: [5],
		  x1: line_start_x, y1: line_start_y,
		  x2: line_start_x + 10, y2: line_end_y,
		});	
		var ruletext = i * max / y_scale;
		var displaytext = "" + ruletext.toFixed(1);
		$('canvas.tj').drawText({
		  layer: true,		  		 
	      fillStyle: '#000',
		  x: line_start_x - 12 - displaytext.length, y: line_start_y,
		  fontSize: 12,
		  fontFamily: fontfamily,
		  text: displaytext,
		});
	}
	//draw y-lengend text
	var lengend_x_start = origin_x - 12 - 30;
	var lengend_y_start = origin_y - y_length / 2;	
	$('canvas.tj').drawText({
	  layer: true,		  		 
	  fillStyle: 'black',
	  x: lengend_x_start, y: lengend_y_start,
	  fontSize: 12,
	  fontFamily: fontfamily,
	  text: legend,
	  rotate: -90
	});
	//draw y-legend text
	var x_start = origin_x + x_length  + 50 - 30;
	var y_start = origin_y - y_length / 2 - 20;
	var STY = new Array("S","T","Y");
	var STY_color = new Array("#CC3333","#66CC00","#3366CC");
	for(var i = 0;i < STY.length;i++){
		$('canvas.tj').drawRect({
		  layer: true,
		  fillStyle: STY_color[i],			  
		  x: x_start, y: y_start,
		  width: 12,
		  height: 12,
		});
		$('canvas.tj').drawText({
		  layer: true,		  		 
		  fillStyle: 'black',
		  x: x_start + 12, y: y_start,
		  fontSize: fontsize - 5,
		  fontFamily: fontfamily,
		  text: STY[i]		  
		});
		y_start = y_start + 16;
	}
}