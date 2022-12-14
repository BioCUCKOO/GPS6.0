var fontsize = 14;
var fontfamily = 'Verdana, sans-serif';

var x_p = 10;			//M氨基酸位点坐标，起始坐标，其他坐标均是该坐标的相对坐标
var y_p = 10;			//M氨基酸位点坐标，起始坐标，其他坐标均是该坐标的相对坐标
var gridwidth = 60;		//y轴网格线宽度

var lengend_x_p = 60;
var lengend_y_p = y_p - 15 - gridwidth * 2 - 25;

function drawAxis(var1,var2){
	var codes = var1;
	var sites = var2;
	//parameters build-in
	var x_origin = 65;		//60
	var y_origin = 190;		//260 坐标轴起始位置
	var gps =new Array();
	for(var i = 0; i < sites.length; i++) {
		var arr = sites[i].split("-");		
		var residue = arr[0];
		gps[i] = parseInt(arr[1]) - 1;
		//alert(gps[i]);
	}
	//origin coordinate
	var center_x = x_origin - fontsize / 2;
	var center_y = y_origin - fontsize / 2 - 5;
	
	var xAxis_x_start = center_x;
	var xAxis_y_start = center_y;	

	//origin start
	var yAxis_x_start = center_x;
	var yAxis_y_start = center_y;	
	
	//draw xAxis
	for(var i = 0; i < codes.length; i++) {
		var xAxis_x_end = xAxis_x_start + fontsize;
		var xAxis_y_end = xAxis_y_start;		
		$('canvas.axis').drawLine({
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
	//$('canvas.axis').drawLine({
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
		$('canvas.axis').drawLine({
		  layer: true,
		  strokeStyle: '#000',
		  strokeWidth: 1,
		  x1: yAxis_x_start, y1: yAxis_y_start,
		  x2: yAxis_x_end, y2: yAxis_y_end,
		  x3: yAxis_x_end - 3, y3: yAxis_y_end,
		});
		$('canvas.axis').drawText({
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
	$('canvas.axis').drawLine({
		 layer: true, strokeStyle: '#000', strokeWidth: 1, x1: center_x, y1: center_y, x2: center_x-5, y2: center_y
	});
	$('canvas.axis').drawText({
		 layer: true, fillStyle: '#000', strokeStyle: '#25a', strokeWidth: 0, x: yAxis_x_end - 13 - 10, y: center_y, fontSize: 12, fontFamily: fontfamily, text: "0",
	});
	
	//draw yAxis arrow -- (yaxis length = 2 * gridwidth + 30)
	//$('canvas.axis').drawLine({
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
		if(gps.indexOf(i) > -1 ){			
			color = 'red';
		}
		$('canvas.axis').drawText({
		  layer: true,
	      fillStyle: color,
		  strokeStyle: '#25a',
		  strokeWidth: 0,
		  //x: x_origin + fontsize * i, y: y_origin,
		  x: x_origin + fontsize * i, y: y_origin,
		  fontSize: fontsize,
		  fontFamily: fontfamily,
		  text: codes[i]
		});	
	}
	
	//draw yAxis threshold line
	var threshold_x_start = center_x;
	var threshold_y_start = center_y - gridwidth * 2 * 0.5;
	var threshold_x_end = threshold_x_start + fontsize * codes.length + 30;
	var threshold_y_end = threshold_y_start;
	$('canvas.axis').drawLine({
	  layer: true,
	  strokeStyle: 'grey',
	  strokeWidth: 1,
	  strokeDash: [5],
	  x1: threshold_x_start, y1: threshold_y_start,
	  x2: threshold_x_end, y2: threshold_y_end,	  
	});
	// $('canvas.axis').drawText({
	  // layer: true,
	  // fillStyle: 'grey',
	  // strokeStyle: '#25a',
	  // strokeWidth: 0,
	  // x: threshold_x_start - 13 - 10, y: threshold_y_start,
	  // fontSize: 12,
	  // fontFamily: fontfamily,
	  // text: "25%"
	// });
}
function drawAsa(var1, var2, var3, var4, var5, var6){
	//drawAsa(codes,disorderValue,'#7CB5EC','#B6E2F5','Disorder region',0);
	var codes = var1;
	var values = var2;
	var linecolor = var3;
	var linecolorlight = var4;
	var title = var5;
	var index = var6;
	var positionValue = "";
	//parameters build-in
	var x_origin = 65;
	var y_origin = 230;
	//draw line	
	for(var i=0;i < codes.length - 1;i++) {
		var value_x_start = x_origin + fontsize * i;
		var value_y_start = y_origin - 52.5 - gridwidth * 2 * values[i];
		var value_x_end = x_origin + fontsize * (i + 1);
		var value_y_end = y_origin - 52.5 - gridwidth * 2 * values[i + 1];		
		var k = values[i + 1];
		var c = codes[i + 1];
		positionValue = positionValue+value_x_end+"_"+value_y_end+":"+k+":"+c+"@";
		$('canvas.axis').drawLine({
		  layer: true,		  
		  strokeStyle: linecolor,
		  strokeWidth: 2,
		  x1: value_x_start, y1: value_y_start,
		  x2: value_x_end, y2: value_y_end,		  
		});
		$('canvas.axis').drawRect({
		  layer: true,			  	 
		  fillStyle: 'white',
		  opacity: 0,
		  strokeStyle: linecolor,
		  strokeWidth: 0,
		  x: value_x_end, y: value_y_end,
		  width: fontsize,
		  height: 100,
		  mouseover: function(layer) {
			$('canvas.axis').drawEllipse({
				layer: true,
				groups: ['myPanel'],
				fillStyle: linecolor,				
				strokeStyle: linecolorlight,
				strokeWidth: 4,
				x: layer.x, y: layer.y,
				width: 16, height: 16
			});
			panel(layer.x,layer.y,"ASA propensity",positionValue, linecolor);			  
		  },
		  mouseout: function() {			  
			$('canvas.axis').removeLayerGroup( 'myPanel' );
		  },		  
		});
		if(index == 0){
			$('canvas.axis').drawEllipse({
			  layer: true,
			  fillStyle: linecolor,
			  x: value_x_end, y: value_y_end,
			  width: 7, height: 7,
			  mouseover: function(layer) {
				$('canvas.axis').drawEllipse({
					layer: true,
					groups: ['myPanel'],
					fillStyle: linecolor,				
					strokeStyle: linecolorlight,
					strokeWidth: 4,
					x: layer.x, y: layer.y,
					width: 16, height: 16
				});
				panel(layer.x,layer.y,"ASA propensity",positionValue, linecolor);	
				
			  },
			  mouseout: function() {			  
				$('canvas.axis').removeLayerGroup( 'myPanel' );
			  },
			});
		}		
		if(index == 1){
			$('canvas.axis').drawPolygon({
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
				panel(layer.x,layer.y,"ASA propensity",positionValue, linecolor);			  
			  },
			  mouseout: function() {			  
				$('canvas.axis').removeLayerGroup( 'myPanel' );
			  },
			});
		}		
	}	
	
	//draw lenged
	var text = var5;
	var lengend_line_x_end = lengend_x_p + 25;
	var lengend_line_y_end = lengend_y_p;
	$('canvas.axis').drawLine({
	  layer: true,
	  strokeStyle: linecolor,
	  strokeWidth: 1,
	  x1: lengend_x_p, y1: lengend_y_p + fontsize / 2,
	  x2: lengend_line_x_end, y2: lengend_line_y_end + fontsize / 2,
	  fromCenter: false
	});
	var lengend_text_x = lengend_line_x_end + 3;
	var lengend_text_y = lengend_y_p;
	$('canvas.axis').drawText({
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

function panel(var1,var2,var3,var4,var5){
	//panel(layer.x,layer.y,"Value",positionValue, linecolor);
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
	var panelWidth = 160;
	var panelHeight = 60;
	var distance_Polygon_rect = 13;		
	$('canvas.axis').drawPolygon({
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
	$('canvas.axis').drawRect({
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
	  index = parseInt((start_x-46)/14)
	  
	$('canvas.axis').drawText({
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
	$('canvas.axis').drawEllipse({
	  layer: true,
	  groups: ['myPanel'],
	  fillStyle: panelcolor,
	  x: start_x - panelWidth/2 + 2 + 10 + 5, y: start_y - distance_Polygon_rect - radius/2 - panelHeight + 6 + fontsize + 7,
	  width: 7, height: 7,	 
	});
	$('canvas.axis').drawText({
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
	$('canvas.axis').drawLayers('myPanel');
}

function drawTitle(){
	//draw Title
	var x_origin = 60;
	var y_origin = 265;
	var text_x = x_origin;
	var text_y = lengend_y_p - fontsize - 40;
	$('canvas.axis').drawText({
	  layer: true,
	  fillStyle: 'black',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: text_x - fontsize / 2, y: y_origin - 255,
	  fontSize: 18 ,
	  fontFamily: fontfamily,
	  text: "Accessible surface area prediction",	
	  fromCenter: false,
	});
}

// canvas
function drawSite(var1,var2,var3){
	var width = var1;
	var length = var2;
	var codes = var3;	
	//parameters build-in
	var height = 30;
	//draw text
	$('canvas.mycanvas').drawText({
	  layer: true,
	  fillStyle: 'black',
	  strokeStyle: '#25a',
	  strokeWidth: 0,
	  x: x_p, y: y_p,
	  fontSize: fontsize + 5,
	  fontFamily: fontfamily,
	  text: "Predicted Site:",	
	  fromCenter: false,
	});
	//draw sequence
	var left_top_rect_x = x_p;
	var left_top_rect_y = y_p + fontsize + 5 + 5;
	var gradient = $('canvas.mycanvas').createGradient({
	  // Gradient is drawn relative to layer position
	  x1: 0, y1: left_top_rect_y + height / 2 - 20,
	  x1: 0, y2: left_top_rect_y + height / 2 + 20,
	  c1: 'grey', s1:0.2,
	  c2: 'white', s2:0.5,
	  c3: 'grey',s3:0.8
	});
	$('canvas.mycanvas').drawRect({
	  layer: true,
	  fillStyle: gradient,
	  x: left_top_rect_x, y: left_top_rect_y,
	  width: width,
	  height: height,
	  fromCenter: false
	});
	//draw start end position
	$('canvas.mycanvas').drawLine({
	  layer: true,
	  strokeStyle: 'black',
	  strokeWidth: 0.8,
	  x1: left_top_rect_x, y1: left_top_rect_y,
	  x2: left_top_rect_x, y2: left_top_rect_y + height + 15,
	});
	$('canvas.mycanvas').drawText({
		layer: true,
		fillStyle: 'black',				
		x: left_top_rect_x, y: left_top_rect_y + height + 15 + fontsize / 2,
		fontSize: fontsize - 7,
		fontFamily: fontfamily,
		text: '1'
	});
	$('canvas.mycanvas').drawLine({
	  layer: true,
	  strokeStyle: 'black',
	  strokeWidth: 0.8,
	  x1: left_top_rect_x + width, y1: left_top_rect_y,
	  x2: left_top_rect_x + width, y2: left_top_rect_y + height + 15,
	});
	$('canvas.mycanvas').drawText({
		layer: true,
		fillStyle: 'black',				
		x: left_top_rect_x + width, y: left_top_rect_y + height + 15 + fontsize / 2,
		fontSize: fontsize - 7,
		fontFamily: fontfamily,
		text: length
	});
	//
	var xoffset = 10;
	var yoffset = 10;
	var max_yoffset = yoffset;
	for(var i=0;i<codes.length;i++) {	
		var arr = codes[i].split("-");		
		var residue = arr[0];
		var site = parseInt(arr[1]);
		var x_site = x_p + site / length * width;
		var y_site = y_p + fontsize + 5 + 5 + height;		
		if(i > 0){
			var previous = codes[i-1].split("-");
			var previous_site = parseInt(previous[1]);
			var x_previous = previous_site / length * width;
			//var distance = codes[i].length * fontsize / 2 + codes[i - 1].length * fontsize / 2;
			//alert(distance);
			if((x_site - x_previous) < 52){
				xoffset = xoffset - 2;
				yoffset = yoffset + fontsize / 2;
			}else{
				xoffset = 10;
				yoffset = 10;
			}
		}		
		if(max_yoffset < yoffset){
			max_yoffset = yoffset;
		}		
		$('canvas.mycanvas').drawLine({
		  layer: true,
		  index: 0,
		  strokeStyle: 'grey',
		  strokeWidth: 1,
		  x1: x_site, y1: y_site,
		  x2: x_site - xoffset, y2: y_site + yoffset,
		  x3: x_site - xoffset, y3: y_site + yoffset + yoffset,
		});
		$('canvas.mycanvas').drawText({
			layer: true,
			fillStyle: 'red',				
			x: x_site - xoffset, y: y_site + yoffset + yoffset + fontsize / 2,
			fontSize: fontsize,
			fontFamily: fontfamily,
			text: residue + (site)
		});
	}
	y_p = y_p + fontsize + 5 + 5 + height + max_yoffset + max_yoffset + fontsize;
}


function drawPieChart2 (var1, var2, var3,var4,var5){
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
	var radius = var5;
	var center_x = x_p + rightoffset;
	var center_y = y_p + 30 + radius;
	//var colors = ['#A5E018','#A52DD4','#11E0B1','#F77617','#82B15C','#E110B5','#CBFA58','#3F124A','#1E7A43'];//the front 8 build-in colors
	var colors = ['#EFE898','#83BB6E','#34b5e2','#42A464','#008B60','#007260','#FFC6A4','#F88F70','#BC5B40'];//the front 8 build-in colors

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
		$('canvas.mycanvas').drawEllipse({
			layer: true,			
			fillStyle: colors[index],
			x: center_x, y: center_y,
			width: radius * 2, height: radius * 2
		});
		$('canvas.mycanvas').drawText({
			layer: true,
			fillStyle: '#000000',   //'#fff',
			x: center_x, y: center_y,
			fontFamily: fontfamily,
			fontSize: fontsize,
			text: names[index] + "\n" + '100' + "%"
		});
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
			//alert(start+" | "+end);
			$('canvas.mycanvas').drawSlice({
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
				$('canvas.mycanvas').drawText({
					layer: true,			
					fillStyle: '#000000',
					x: x, y: y,
					fontFamily: fontfamily,
					//fontSize: fontsize - 10,
					fontSize: fontsize,
					text: names[i] + "\n" + percent + "%"
				})
			}		
		}
	}
	//draw legend
	var lengend_x_start = center_x;
	var lengend_y_start = center_y - radius - 20;
	$('canvas.mycanvas').drawText({
	  layer: true,		  		 
	  fillStyle: 'black',
	  x: lengend_x_start, y: lengend_y_start,
	  fontSize: fontsize,
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
	var deep = 220;	
	var x_length = 260;	//x-axis length width
	var y_length = 180;	//y-axis length width
	var barwidth = 18;	//bar width
	var y_scale = 2;	//y-axis scale number
	
	//origin coordinate
	var origin_x = x_p + rightoffset;	// refer the origin coordinate is ok
	var origin_y = y_p + deep;				// refer the origin coordinate is ok
		
	//x axis end 
	var xAxis_x_end = origin_x + x_length;
	var xAxis_y_end = origin_y;	
	//y axis end 
	var yAxis_x_end = origin_x;
	var yAxis_y_end = origin_y - y_length;	
	
	//draw xAxis
	$('canvas.mycanvas').drawLine({
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
	$('canvas.mycanvas').drawLine({
		 layer: true, strokeStyle: '#000', strokeWidth: 2, x1: origin_x + x_length/2, y1: origin_y,x2: origin_x + x_length/2, y2: origin_y+10,
	});
	$('canvas.mycanvas').drawLine({
		 layer: true, strokeStyle: '#000', strokeWidth: 2, x1: origin_x + x_length, y1: origin_y,x2: origin_x + x_length, y2: origin_y+10,
	});
	//draw yAxis
	$('canvas.mycanvas').drawLine({
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
	$('canvas.mycanvas').drawText({
	  layer: true, fillStyle: '#000', x: origin_x-20 , y: origin_y,//text downoffset
	  fontSize: 12,
	  fontFamily: fontfamily,
	  text: "0.0",
	});
	$('canvas.mycanvas').drawLine({
		 layer: true, strokeStyle: 'black', strokeWidth: 2, x1: origin_x, y1: origin_y,x2: origin_x-6, y2: origin_y,
	});
	//draw bar	
	var x_step = x_length / values.length;
	//var color = new Array("#c33","#6c0","#36c");
	var color = new Array('#FFE081','#5EC27E','#00C9CC');
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
	//alert(max);
	for(var i =0; i < values.length;i++){
		var arr = values[i];		
		var position_x = origin_x + x_step * (i + 1) - barwidth * arr.length / 2-50;		
		for(var j =0; j < arr.length;j++){
			var Coloum_x_start = position_x + j * barwidth;
			var Coloum_y_start = origin_y - (arr[j] / max) * y_length / 2;
			var height = (arr[j] / max) * y_length;			
			$('canvas.mycanvas').drawRect({
			  layer: true,
			  fillStyle: color[j],			  
			  x: Coloum_x_start, y: Coloum_y_start,
			  width: barwidth,
			  height: height,
			});
		}
		//draw x axis name
		$('canvas.mycanvas').drawText({
		  layer: true,		  		 
	      fillStyle: '#0088FF',
		  x: position_x + barwidth * arr.length / 2, y: origin_y + 12,//text downoffset
		  fontSize: fontsize,
		  fontFamily: fontfamily,
		  text: names[i],
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
		$('canvas.mycanvas').drawLine({
		  layer: true,
		  strokeStyle: '#000',
		  strokeWidth: 2,
		  strokeDash: [5],
		  x1: origin_x, y1: line_start_y,
		  x2: origin_x - 10, y2: line_end_y,
		});	
		var ruletext = i * max / y_scale;
		var displaytext = "" + ruletext.toFixed(1);
		$('canvas.mycanvas').drawText({
		  layer: true,		  		 
	      fillStyle: '#000',
		  x: line_start_x - 12 - displaytext.length, y: line_start_y,
		  fontSize: 12,
		  fontFamily: fontfamily,
		  text: displaytext,
		});
	}
	//draw y-legend text
	var lengend_x_start = origin_x - 12 - 30;
	var lengend_y_start = origin_y - y_length / 2;	
	$('canvas.mycanvas').drawText({
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
	//var STY_color = new Array("#CC3333","#66CC00","#3366CC");
	var STY_color = new Array('#FFE081','#5EC27E','#00C9CC');
	for(var i = 0;i < STY.length;i++){
		$('canvas.mycanvas').drawRect({
		  layer: true,
		  fillStyle: STY_color[i],			  
		  x: x_start, y: y_start,
		  width: 12,
		  height: 12,
		});
		$('canvas.mycanvas').drawText({
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

function getwidth(codes){
	var width = 130 + codes.length * fontsize;
	return width;
}