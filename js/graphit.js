/***********************************************************************
* graphit.js                                                           *
*                                                                      *
* This script implement all the logic behind the GraphIt! application. *
*                                                                      *
* Author: Jose Aguilar-Canepa                                          *
* Version: 0.5 alpha                                                   *
*                                                                      *
* Version history:                                                     *
*                                                                      *
* - 0.5a:                                                              *
*     - Added the option to load graphs in JSON format, as defined by  *
*         the Java Graph Viewer Engine.                                *
*                                                                      *
* - 0.4a:                                                              *
*     - Added the action to delete vertex's neighborhoods.             *
*     - Corrected an error with the 'Force direction' edge smoothness  *
*         option.                                                      *
*                                                                      *
* - 0.3a:                                                              *
*     - Added multi-selection support for nodes: now more than one     *
*         node can be selected and modified at the same time.          *
*     - Added multi-selection support for edges: now more than one     *
*         edge can be selected and modified at the same time.          *
*     - Added the panel to modify the graph.                           *
*     - Added the action to create subgraphs.                          *
*     - Added the action to create neighbor-subgraphs.                 *
*                                                                      *
* - 0.2a:                                                              *
*     - Added the panel to modify global node options.                 *
*     - Added the panel to modify global edge options.                 *
*                                                                      *
* - 0.1a:                                                              *
*     - Added the panel to add new nodes.                              *
*     - Added the panel to add new edges.                              *
*     - Added the panel to modify basic node information.              *
*     - Added the panel to modify basic edge information.              *
***********************************************************************/

"use strict";

/** This is the array of fonts supported by the application. */
var FONTS = [
    '"Lucida Sans Unicode", "Lucida Grande", sans-serif',
    '"Trebuchet MS", Helvetica, sans-serif',
    'Tahoma, Geneva, sans-serif',
    'Verdana, Geneva, sans-serif',
    'Impact, Charcoal, sans-serif',
    'Arial, Helvetica, sans-serif',
    '"Comic Sans MS", cursive, sans-serif',
    'Georgia, serif',
    '"Palatino Linotype", "Book Antiqua", Palatino, serif',
    '"Times New Roman", Times, serif',
    '"Courier New", Courier, monospace',
    '"Lucida Console", Monaco, monospace'
];

/** This is the Object used to store the graph's elements. */
var data = null;

/** This is the DataSet object used to store the graph's nodes. */
var nodes = null;

/** This is the DataSet object used to store the graph's edges. */
var edges = null;

/** This is the Network object that represents the graph itself. */
var graph = null;

/** This is the DOM component in which the graph is drawed. */
var canvas = null;

/** This is the Object used to store the graph's configuration. */
var options = null;

/** This variable indicates the node selection node. */
var multNode = false;

/** This variable indicates the edge selection node. */
var multEdge = false;

/**
* Initializes the application.
*
* This method is called whenever the page is loaded.
*
* æreturns {void} nothing.
*/
function init() {
    // Create the JQueryUI widgets.
    $('input').tooltip();
    $('select').tooltip();
    $('#ctrl-tabs').tabs();
    
    $('#subg-btn').tooltip().click(function(event){
        event.preventDefault();
        createSubgraph();
    });

    $('#nsbg-btn').tooltip().click(function(event) {
        event.preventDefault();
        createNeighborSubgraph();
    });
    
    $('#dngh-btn').tooltip().click(function(event) {
        event.preventDefault();
        deleteNeighbors();
    });
    
    $('.slider').slider({
        min: 0,
        max: 100,
        step: 1,
        value: 50
    }).tooltip();

    $('.ctrl-accordion').accordion({
        active: false,
        collapsible: true,
        heightStyle: "content"
    });

    $('.ctrl-subaccordion').accordion({
        active: false,
        collapsible: true,
        heightStyle: "content"
    });

    $('.ctrl-btn').button().click(function(event) {
        event.preventDefault();
    });

    // Add the handlers to the sliders
    $('#gnod-shadow-alpha').on('slide', function(event, ui) {
        var picker = document.getElementById('gnod-shadow-color').jscolor;
        changeGlobalNodeShadowColor(picker);
    });

    $('#gedg-shadow-alpha').on('slide', function(event, ui) {
        var picker = document.getElementById('gedg-shadow-color').jscolor;
        changeGlobalEdgeShadowColor(picker);
    });
    
    $('#gedg-acolor').on('slide', function(event, ui) {
        graph.setOptions({
            edges: {
                color: {
                    opacity: parseFloat($(this).slider('value')) / 100.0
                }
            }
        });
    });
    
    $('#gedg-smooth-roundness').on('slide', function(event, ui) {
        if($('#gedg-smooth').prop('checked'))
            graph.setOptions({
                edges: {
                    smooth: {
                        roundness: parseFloat($(this).slider('value')) / 100.0
                    }
                }
            });
    });

    // Initialize the global variables
    canvas = document.getElementById("graph");
    nodes = new vis.DataSet([]);
    edges = new vis.DataSet([]);

    // Add event listeners to UI components.
    $('#anod-btn').click(addNode);
    $('#aedg-btn').click(addEdge);
    $('#dnod-btn').click(deleteNode);
    $('#dedg-btn').click(deleteEdge);
    $('#mnod-btn').click(modifyNode);
    $('#medg-btn').click(modifyEdge);
    
    $('#dimacs-inp').change(function(event) {
        openDIMACS(event);
    });
    
    $('#json-inp').change(function(event) {
        openJSON(event);
    });

    // Create the handlers for the options 
    
    // -------------------- Global Node Appearance Options --------------------
    $('#gnod-shape').change(function() {
        // Only certain shapes allow to change size
        var shape = $(this).val();
        var allowSize = (shape === 'diamond') || (shape === 'dot') 
          || (shape === 'star') || (shape === 'triangle') 
          || (shape === 'triangleDown') || (shape === 'square');
          
        graph.setOptions({
            nodes: {
                shape: shape,
                size: allowSize ? parseInt($('#gnod-size').val()) : 1
            }
        });
        
        $('#gnod-size').prop('disabled', !allowSize);
        allowSize ? $('#gnod-lblsize').show() : $('#gnod-lblsize').hide();
        allowSize ? $('#gnod-size').show() : $('#gnod-size').hide();
        
    });

    $('#gnod-size').change(function() {
        var newSize = $(this).val();

        if(newSize === '') {
            newSize = 25;
            $(this).val(newSize);
        }

        graph.setOptions({
            nodes: {
                size: parseInt(newSize)
            }
        });
        
        graph.redraw();
    });

    $('#gnod-hidden').change(function() {
        graph.setOptions({
            nodes: {
                hidden: $(this).prop('checked')
            }
        });
    });

    // ---------------------- Global Node Border Options ----------------------
    $('#gnod-border-width').change(function() {
        graph.setOptions({
            nodes: {
                borderWidth: parseInt($(this).val())
            }
        });
    });

    $('#gnod-border-swidth').change(function() {
        graph.setOptions({
            nodes: {
                borderWidthSelected: parseInt($(this).val())
            }
        });
    });

    $('#gnod-border-radius').change(function() {
        graph.setOptions({
            nodes: {
                shapeProperties: {
                    borderRadius: parseInt($(this).val())
                }
            }
        });
    });

    $('#gnod-border-dashes').change(function() {
        graph.setOptions({
            nodes: {
                shapeProperties: {
                    borderDashes: $(this).prop('checked') ? [5, 5] : false
                }
            }
        });
    });

    // ----------------------- Global Node Font Options -----------------------
    $('#gnod-font-face').change(function() {
        graph.setOptions({
            nodes: {
                font: {
                    face: FONTS[parseInt($(this).val())]
                }
            }
        });
    });

    $('#gnod-font-size').change(function() {
        graph.setOptions({
            nodes: {
                font: {
                    size: parseInt($(this).val())
                }
            }
        });
    });

    $('#gnod-font-sbold').change(function() {
        graph.setOptions({
            nodes: {
                labelHighlightBold: $(this).prop('checked')
            }
        });
    });

    $('#gnod-font-bg').change(function() {
        var picker = document.getElementById('gnod-font-bgcolor');
        var checked = $(this).prop('checked');
        var bglbl = $('#gnod-font-lblbgcolor');
        var bginp = $('#gnod-font-bgcolor');

        // Shows/hides the font bg color selector
        checked ? bglbl.show() : bglbl.hide();
        checked ? bginp.show() : bginp.hide();

        graph.setOptions({
            nodes: {
                font: {
                    background: checked ? picker.jscolor.toHEXString() : 'none'
                }
            }
        });
    });

    $('#gnod-font-stroke').change(function() {
        var picker = document.getElementById('gnod-font-skcolor');
        var checked = $(this).prop('checked');
        var sklblw = $('#gnod-font-lblskwidth');
        var skinpw = $('#gnod-font-skwidth');
        var sklblc = $('#gnod-font-lblskcolor');
        var skinpc = $('#gnod-font-skcolor');
        
        // Shows/hides the stroke options
        checked ? sklblw.show() : sklblw.hide();
        checked ? skinpw.show() : skinpw.hide();
        checked ? sklblc.show() : sklblc.hide();
        checked ? skinpc.show() : skinpc.hide();

        graph.setOptions({
            nodes: {
                font: {
                    strokeWidth: checked ? parseInt($('#gnod-font-skwidth').val()) : 0,
                    strokeColor: picker.jscolor.toHEXString()
                }
            }
        });
    });

    $('#gnod-font-skwidth').change(function() {
        if($('#gnod-font-stroke').prop('checked'))
            graph.setOptions({
                nodes: {
                    font: {
                        strokeWidth: parseInt($(this).val())
                    }
                }
            });
    });
    
    // -------------------- --Global Node Physics Options ---------------------
    $('#gnod-physics').change(function() {
        graph.setOptions({
            nodes: {
                physics: $(this).prop('checked')
            }
        });
    });

    $('#gnod-mass').change(function() {
        var newMass = $(this).val();

        if(newMass === '' || newMass === ' ') {
            newMass = 1;
            $(this).val(newMass);
        }

        graph.setOptions({
            nodes: {
                mass: parseInt($(this).val())
            }
        });
    });

    $('#gnod-fixed').change(function() {
        var x = $('#gnod-fixed-x');
        var lblx = $('#gnod-fixed-lblx');
        var y = $('#gnod-fixed-y');
        var lbly = $('#gnod-fixed-lbly');
        var checked = $(this).prop('checked');
        
        $('#gnod-fixed-x').prop('checked', checked);
        $('#gnod-fixed-y').prop('checked', checked);

        checked ? x.show() : x.hide();
        checked ? lblx.show() : lbly.hide();
        checked ? y.show() : y.hide();
        checked ? lbly.show() : lbly.hide();

        graph.setOptions({
            nodes: {
                fixed: {
                    x: checked,
                    y: checked
                }
            }
        });
    });

    $('#gnod-fixed-x').change(function() {
        var x = $('#gnod-fixed-x');
        var lblx = $('#gnod-fixed-lblx');
        var y = $('#gnod-fixed-y');
        var lbly = $('#gnod-fixed-lbly');
        var checkedX = $(this).prop('checked');
        var checkedY = $('#gnod-fixed-y').prop('checked');

        $('#gnod-fixed').prop('checked', (checkedX || checkedY));

        (checkedX || checkedY) ? x.show() : x.hide();
        (checkedX || checkedY) ? lblx.show() : lblx.hide();
        (checkedX || checkedY) ? y.show() : y.hide();
        (checkedX || checkedY) ? lbly.show() : lbly.hide();

        graph.setOptions({
            nodes: {
                fixed: {
                    x: checkedX,
                    y: checkedY
                }
            }
        });
    });

    $('#gnod-fixed-y').change(function() {
        var x = $('#gnod-fixed-x');
        var lblx = $('#gnod-fixed-lblx');
        var y = $('#gnod-fixed-y');
        var lbly = $('#gnod-fixed-lbly');
        var checkedY = $(this).prop('checked');
        var checkedX = $('#gnod-fixed-x').prop('checked');

        $('#gnod-fixed').prop('checked', (checkedY || checkedX));

        (checkedX || checkedY) ? x.show() : x.hide();
        (checkedX || checkedY) ? lblx.show() : lblx.hide();
        (checkedX || checkedY) ? y.show() : y.hide();
        (checkedX || checkedY) ? lbly.show() : lbly.hide();

        graph.setOptions({
            nodes: {
                fixed: {
                    x: checkedX,
                    y: checkedY
                }
            }
        });
    });

    // ---------------------- Global Node Shadow Options ----------------------
    $('#gnod-shadow').change(function() {
        var checked = $(this).prop('checked');
        var lblalpha = $('#gnod-shadow-lblalpha');
        var inpalpha = $('#gnod-shadow-alpha');
        var lblcolor = $('#gnod-shadow-lblcolor');
        var inpcolor = $('#gnod-shadow-color');
        var lblsize = $('#gnod-shadow-lblsize');
        var inpsize = $('#gnod-shadow-size');
        var lblx = $('#gnod-shadow-lblx');
        var inpx = $('#gnod-shadow-x');
        var lbly = $('#gnod-shadow-lbly');
        var inpy = $('#gnod-shadow-y');
        
        // Shows/hides the shadow options.
        checked ? lblalpha.show() : lblalpha.hide();
        checked ? inpalpha.show() : inpalpha.hide();
        checked ? lblcolor.show() : lblcolor.hide();
        checked ? inpcolor.show() : inpcolor.hide();
        checked ? lblsize.show() : lblsize.hide();
        checked ? inpsize.show() : inpsize.hide();
        checked ? lblx.show() : lblx.hide();
        checked ? inpx.show() : inpx.hide();
        checked ? lbly.show() : lbly.hide();
        checked ? inpy.show() : inpy.hide();
        
        graph.setOptions({
            nodes: {
                shadow: {
                    enabled: $(this).prop('checked')
                }
            }
        });

        if($(this).prop('checked')) {
            jscolor = document.getElementById('gnod-shadow-color').jscolor;
            changeGlobalNodeShadowColor(jscolor);
        }
    });

    $('#gnod-shadow-size').change(function() {
        var newSize = $(this).val();

        if(newSize === '' || newSize === ' ') {
            newSize = 10;
            $(this).val(newSize);
        }

        if($('#gnod-shadow').prop('checked')) {
            graph.setOptions({
                nodes: {
                    shadow: { 
                        size: parseInt(newSize)
                    }
                }
            });
        }
    });

    $('#gnod-shadow-x').change(function() {
        var newX = $(this).val();

        if(newX === '' || newX === ' ') {
            newX = 5;
            $(this).val(newX);
        }

        if($('#gnod-shadow').prop('checked')) {
            graph.setOptions({
                nodes: {
                    shadow: {
                        x: parseInt(newX)
                    }
                }
            });
        }
    });

    $('#gnod-shadow-y').change(function() {
        var newY = $(this).val();

        if(newY === '' || newY === ' ') {
            newY = 5;
            $(this).val(newY);
        }

        if($('#gnod-shadow').prop('checked')) {
            graph.setOptions({
                nodes: {
                    shadow: {
                        y: parseInt(newY)
                    }
                }
            });
        }
    });

    // -------------------- Global Edge Appearance Options -------------------
    $('#gedg-dashes').change(function() {
        graph.setOptions({
            edges: {
                dashes: $(this).prop('checked')
            }
        });
    });

    $('#gedg-hidden').change(function() {
        graph.setOptions({
            edges: {
                hidden: $(this).prop('checked')
            }
        });
    });

    $('#gedg-physics').change(function() {
        graph.setOptions({
            edges: {
                physics: $(this).prop('checked')
            }
        });
    });

    $('#gedg-width').change(function() {
        var width = $(this).val();

        if(width === '' || width === ' ') {
            width = 1;
            $(this).val(width);
        }

        graph.setOptions({
            edges: {
                width: parseInt(width)
            }
        });
    });

    // ---------------------- Global Edge Arrows Options ---------------------
    $('#gedg-arrows-to').change(function() {
        var checked = $(this).prop('checked');
        var label = $('#gedg-arrows-lbltscale');
        var scale = $('#gedg-arrows-tscale');
        
        checked ? label.show() : label.hide();
        checked ? scale.show() : scale.hide();
        
        graph.setOptions({
            edges: {
                arrows: {
                    to: {
                        enabled: checked,
                        scaleFactor: checked ? parseInt(scale.val()) : 1
                    }
                }
            }
        });
    });

    $('#gedg-arrows-tscale').change(function() {
        var scale = $(this).val();

        if(scale === '' || scale === ' ') {
            scale = 1;
            $(this).val(scale);
        }

        if($('#gedg-arrows-to').prop('checked'))
            graph.setOptions({
                edges: {
                    arrows: {
                        to: {
                            scaleFactor: parseInt(scale)
                        }
                    }
                }
            });
    });

    $('#gedg-arrows-middle').change(function() {
        var checked = $(this).prop('checked');
        var label = $('#gedg-arrows-lblmscale');
        var scale = $('#gedg-arrows-mscale');
        
        checked ? label.show() : label.hide();
        checked ? scale.show() : scale.hide();
        
        graph.setOptions({
            edges: {
                arrows: {
                    middle: {
                        enabled: checked,
                        scaleFactor: checked ? parseInt(scale.val()) : 1
                    }
                }
            }
        });
    });

    $('#gedg-arrows-mscale').change(function() {
        var scale = $(this).val();

        if(scale === '' || scale === ' ') {
            scale = 1;
            $(this).val(scale);
        }

        if($('#gedg-arrows-middle').prop('checked')) 
            graph.setOptions({
                edges: {
                    arrows: {
                        middle: {
                            scaleFactor: parseInt(scale)
                        }
                    }
                }
            });
    });

    $('#gedg-arrows-from').change(function() {
        var checked = $(this).prop('checked');
        var label = $('#gedg-arrows-lblfscale');
        var scale = $('#gedg-arrows-fscale');
        
        checked ? label.show() : label.hide();
        checked ? scale.show() : scale.hide();
        
        graph.setOptions({
            edges: {
                arrows: {
                    from: {
                        enabled: checked,
                        scaleFactor: checked ? parseInt(scale.val()) : 1
                    }
                }
            }
        });
    });

    $('#gedg-arrows-fscale').change(function() {
        var scale = $(this).val();

        if(scale === '' || scale === ' ') {
            scale = 1;
            $(this).val(scale);
        }

        if($('#gedg-arrows-from').prop('checked'))
            graph.setOptions({
                edges: {
                    arrows: {
                        from: {
                            scaleFactor: parseInt(scale)
                        }
                    }
                }
            });
    });

    $('#gedg-arrows-strikethrough').change(function() {
        graph.setOptions({
            edges: {
                arrowStrikethrough: $(this).prop('checked')
            }
        });
    });

    // ---------------------- Global Edge Color Options ----------------------
    $('#gedg-icolor').change(function() {
        var color = $('#gedg-color');
        var lblcolor = $('#gedg-lblcolor');
        var hover = $('#gedg-hcolor');
        var lblhover = $('#gedg-lblhcolor');
        var selected = $('#gedg-scolor');
        var lblselected = $('#gedg-lblscolor');
        var showColor = $(this).val() === 'none';
        var jscolor = document.getElementById('gedg-color').jscolor;
        var hscolor = document.getElementById('gedg-hcolor').jscolor;
        var sscolor = document.getElementById('gedg-scolor').jscolor;
        
        showColor ? color.show() : color.hide();
        showColor ? lblcolor.show() : lblcolor.hide();
        showColor ? hover.show() : hover.hide();
        showColor ? lblhover.show() : lblhover.hide();
        showColor ? selected.show() : selected.hide();
        showColor ? lblselected.show() : lblselected.hide();
       
        if(showColor)
            graph.setOptions({
                edges: {
                    color: {
                        color: jscolor.toHEXString(),
                        highlight: sscolor.toHEXString(),
                        hover: hscolor.toHEXString(),
                        inherit: false
                    }
                }
            });
        else 
            graph.setOptions({
                edges: {
                    color: {
                        inherit: $(this).val()
                    }
                }
            });
    });

    // ----------------------- Global Edge Font Options ----------------------
    $('#gedg-font-face').change(function() {
        graph.setOptions({
            edges: {
                font: {
                    face: FONTS[parseInt($(this).val())]
                }
            }
        });
    });
    
    $('#gedg-font-size').change(function() {
        graph.setOptions({
            edges: {
                font: {
                    size: parseInt($(this).val())
                }
            }
        });
    });

    $('#gedg-label-sbold').change(function() {
        graph.setOptions({
            edges: {
                labelHighlightBold: $(this).prop('checked')
            }
        });
    });

    $('#gedg-font-bg').change(function() {
        var color = $('#gedg-font-bgcolor');
        var label = $('#gedg-font-lblbgcolor');
        var checked = $(this).prop('checked');
        var jscolor = document.getElementById('gedg-font-bgcolor').jscolor;
        
        checked ? label.show() : label.hide();
        checked ? color.show() : color.hide();
        
        graph.setOptions({
            edges: {
                font: {
                    background: checked ? jscolor.toHEXString() : 'none'
                }
            }
        });
    });

    $('#gedg-font-stroke').change(function() {
        var color = $('#gedg-font-skcolor');
        var lblcolor = $('#gedg-font-lblskcolor');
        var width = $('#gedg-font-skwidth');
        var lblwidth = $('#gedg-font-lblskwidth');
        var checked = $(this).prop('checked');
        var jscolor = document.getElementById('gedg-font-skcolor').jscolor;
        
        checked ? color.show() : color.hide();
        checked ? lblcolor.show() : lblcolor.hide();
        checked ? width.show() : width.hide();
        checked ? lblwidth.show() : lblwidth.hide();
        
        if(checked)
            graph.setOptions({
                edges: {
                    font: {
                        strokeWidth: parseInt(width.val()),
                        strokeColor: jscolor.toHEXString()
                    }
                }
            });
        else
            graph.setOptions({
                edges: {
                    font: {
                        strokeWidth : 0
                    }
                }
            });
    });

    $('#gedg-font-skwidth').change(function() {
        var width = $(this).val();

        if(width === '' || width === ' ') {
            width = 2;
            $(this).val(width);
        }

        if($('#gedg-font-stroke').prop('checked'))
            graph.setOptions({
                edges: {
                    font: {
                        strokeWidth: parseInt(width)
                    }
                }
            });
    });

    // ---------------------- Global Edge Shadow Options ----------------------
    $('#gedg-shadow').change(function() {
        var color = $('#gedg-shadow-color');
        var lblcolor = $('#gedg-shadow-lblcolor');
        var alpha = $('#gedg-shadow-alpha');
        var lblalpha = $('#gedg-shadow-lblalpha');
        var size = $('#gedg-shadow-size');
        var lblsize = $('#gedg-shadow-lblsize');
        var x = $('#gedg-shadow-x');
        var lblx = $('#gedg-shadow-lblx');
        var y = $('#gedg-shadow-y');
        var lbly = $('#gedg-shadow-lbly');
        var checked = $(this).prop('checked');
        var picker = document.getElementById('gedg-shadow-color').jscolor;

        checked ? color.show() : color.hide();
        checked ? lblcolor.show() : lblcolor.hide();
        checked ? alpha.show() : alpha.hide();
        checked ? lblalpha.show() : lblalpha.hide();
        checked ? size.show() : size.hide();
        checked ? lblsize.show() : lblsize.hide();
        checked ? x.show() : x.hide();
        checked ? lblx.show() : lblx.hide();
        checked ? y.show() : y.hide();
        checked ? lbly.show() : lbly.hide();

        if(checked) 
            changeGlobalEdgeShadowColor(picker);
        else 
            graph.setOptions({
                edges: {
                    shadow: {
                        enabled: false
                    }
                }
            });
    });

    $('#gedg-shadow-size').change(function() {
        var size = $(this).val();

        if(size === '' || size === ' ') {
            size = 10;
            $(this).val(size);
        }

        if($('#gedg-shadow').prop('checked'))
            graph.setOptions({
                edges: {
                    shadow: {
                        size: parseInt(size)
                    }
                }
            });
    });

    $('#gedg-shadow-x').change(function() {
        var x = $(this).val();

        if(x === '' || x === ' ') {
            x = 5;
            $(this).val(x);
        }

        if($('#gedg-shadow').prop('checked'))
            graph.setOptions({
                edges: {
                    shadow: {
                        x: parseInt(x)
                    }
                }
            });
    });

    $('#gedg-shadow-y').change(function() {
        var y = $(this).val();

        if(y === '' || y === ' ') {
            y = 5;
            $(this).val(y);
        }

        if($('#gedg-shadow').prop('checked'))
            graph.setOptions({
                edges: {
                    shadow: {
                        y: parseInt(y)
                    }
                }
            });
    });
    
    // -------------------- Global Edge Smoothness Options -------------------
    $('#gedg-smooth').change(function(){
        var type = $('#gedg-smooth-type');
        var lbltype = $('#gedg-smooth-lbltype');
        var force = $('#gedg-smooth-forcedir');
        var lblforce = $('#gedg-smooth-lblforcedir');
        var roundness = $('#gedg-smooth-roundness');
        var lblroundness = $('#gedg-smooth-lblroundness');
        var checked = $(this).prop('checked');
        
        checked ? type.show() : type.hide();
        checked ? lbltype.show() : lbltype.hide();
        checked ? force.show() : force.hide();
        checked ? lblforce.show() : lblforce.hide();
        checked ? roundness.show() : roundness.hide();
        checked ? lblroundness.show() : lblroundness.hide();
        
        if(checked)
            graph.setOptions({
                edges: {
                    smooth: {
                        enabled: true,
                        type: type.val(),
                        forceDirection: force.val(),
                        roundness: parseFloat(roundness.slider('value')) / 100.0
                    }
                }
            });
        else
            graph.setOptions({
                edges: {
                    smooth: {
                        enabled: false
                    }
                }
            });
    });
    
    $('#gedg-smooth-type').change(function() {
        if($('#gedg-smooth').prop('checked'))
            graph.setOptions({
                edges: {
                    smooth: {
                        type: $(this).val()
                    }
                }
        });
    });
    
    $('#gedg-smooth-forcedir').change(function() {
        if($('#gedg-smooth').prop('checked'))
            graph.setOptions({
                edges: {
                    smooth: {
                        forceDirection: $(this).val()
                    }
                }
            });
    });

    createNetwork();
}

/**
* Add an edge to the graph.
*
* @returns {void} nothing.
*/
function addEdge() {
    var newEdge = {
        from: parseInt($('#aedg-from').val()),
        to: parseInt($('#aedg-to').val())
    }

    edges.add(newEdge);
}

/**
* Add a node to the graph.
*
* @returns {void} nothing.
*/
function addNode() {
    var picker = document.getElementById('anod-color').jscolor;
    
    var newNode = {
        id: parseInt($('#anod-id').val()),
        label: $('#anod-label').val(),
        color: picker.toHEXString()
    }

    nodes.add(newNode);
}

/**
* Build the "options" Object that customize the appearance of the graph.
*
* The options created by the method are the default options defined in
* the visjs documentation. Please refer to the documentation in
* http://visjs.org/docs/network/nodes.html to read about the effect of
* every option.
*
* @returns {void} nothing.
*/
function buildOptions() {
    options = {
        // Node options
        nodes: {
            borderWidth: 1,
            borderWidthSelected: 2,
            hidden: false,
            mass: 1,
            physics: false,
            shape: "ellipse",
            size: 25,

            color: {
                border: "#2B7CE9",
                background: "#97C2FC",
                highlight: {
                    border: "#2B7CE9",
                    background: "#D2E5FF"
                },
                hover: {
                    border: "#2B7CE9",
                    background: "#D2E5FF"
                }
            },

            fixed: {
                x: false,
                y: false
            },

            font: {
                color: "#343434",
                size: 14,
                face: '"Lucida Sans Unicode", "Lucida Grande", sans-serif',
                background: "none",
                strokeWidth: 0,
                strokeColor: "#FFFFFF"
            },

            shadow: {
                enabled: false,
                color: "rgba(0, 0, 0, 0.5)",
                size: 10,
                x: 5,
                y: 5
            },

            shapeProperties: {
                borderDashes: false,
                borderRadius: 6
            }
        },

        edges: {
            arrowStrikethrough : true,
            dashes: false,
            hidden: false,
            labelHighlightBold: true,
            physics: false,
            width: 1,

            arrows: {
                to: {
                    enabled: false,
                    scaleFactor: 1
                },

                middle: {
                    enabled: false,
                    scaleFactor: 1
                },

                from: {
                    enabled: false,
                    scaleFactor: 1
                }
            },

            color: {
                color: "#848484",
                highlight: "#848484",
                hover: "#848484",
                inherit: false,
                opacity: 1.0
            },
            
            smooth: {
                enabled: false
            }
        },

        interaction: {
            hover: true,
            multiselect: true
        }
    }
}

/**
* Change the global edge color defined in the graph's "options" Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalEdgeColor(jscolor) {
    graph.setOptions({
        edges: {
            color: {
                color: jscolor.toHEXString()
            }
        }
    });
}

/**
* Change the global edge font background color defined in the graph's
* "options" Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalEdgeFontBackgroundColor(jscolor) {
    if($('#gedg-font-bg').prop('checked'))
        graph.setOptions({
            edges: {
                font: {
                    background: jscolor.toHEXString()
                }
            }
        });
}

/**
* Change the global edge font color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalEdgeFontColor(jscolor) {
    graph.setOptions({
        edges: {
            font: {
                color: jscolor.toHEXString()
            }
        }
    });
}

/**
* Change the global edge font color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor 
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*/
function changeGlobalEdgeFontStrokeColor(jscolor) {
    if($('#gedg-font-stroke').prop('checked'))
        graph.setOptions({
            edges: {
                font: {
                    strokeColor: jscolor.toHEXString()
                }
            }
        });
}

/**
* Change the global edge highlight color defined in the graph's 
* "options" Object.
*
* This method is directly called from the corresponding jscolor 
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
* picker.
*
* @returns {void} nothing.
*/
function changeGlobalEdgeHighlightColor(jscolor) {
    graph.setOptions({
        edges: {
            color: {
                highlight: jscolor.toHEXString()
            }
        }
    });
}

/**
* Change the global edge hover color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalEdgeHoverColor(jscolor) {
    graph.setOptions({
        edges: {
            color: {
                hover: jscolor.toHEXString()
            }
        }
    });
}

/**
* Change the global edge shadow color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} picker the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalEdgeShadowColor(picker) {
    var color = picker.toRGBString();
    var alpha = $('#gedg-shadow-alpha').slider('value');
    color = color.replace('rgb', 'rgba');
    color = color.replace(')', ',' + (parseFloat(alpha) / 100.0).toString() + ')');

    if($('#gedg-shadow').prop('checked'))
        graph.setOptions({
            edges: {
                shadow: {
                    enabled: true,
                    color: color
                }
            }
        });
}

/**
* Change the global node border color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeBorderColor(jscolor) {
    graph.setOptions({
        nodes: {
            color: {
                border: jscolor.toHEXString()
            }
        }
    });
}

/**
* Change the global node border highlight color defined in the graph's
* "options" Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeBorderHighlightColor(jscolor) {
    graph.setOptions({
        nodes: {
            color: {
                highlight: {
                    border: jscolor.toHEXString()
                }
            }
        }
    });
}

/**
* Change the global node border hover color defined in the graph's
* "options" Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeBorderHoverColor(jscolor) {
    graph.setOptions({
        nodes: {
            color: {
                hover: {
                    border: jscolor.toHEXString()
                }
            }
        }
    });
}

/**
* Change the global node color defined in the graph's "options" Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeColor(jscolor) {
    graph.setOptions({
        nodes: {
            color: {
                background: jscolor.toHEXString()
            }
        }
    });
}

/**
* Change the global node font background color defined in the graph's
* "options" Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeFontBackground(jscolor) {
    if($('#gnod-font-bg').prop('checked'))
        graph.setOptions({
            nodes: {
                font: {
                    background: jscolor.toHEXString()
                }
            }
        });
}

/**
* Change the global node font color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeFontColor(jscolor) {
    graph.setOptions({
        nodes: {
            font: {
                color: jscolor.toHEXString()
            }
        }
    });
}

/**
* Change the global node font color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeFontStroke(jscolor) {
    if($('#gnod-font-stroke').prop('checked'))
        graph.setOptions({
            nodes: {
                font: {
                    strokeColor: jscolor.toHEXString()
                }
            }
        });
}

/**
* Change the global node highlight color defined in the graph's
* "options" Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeHighlightColor(jscolor) {
    graph.setOptions({
        nodes: {
            color: {
                highlight: {
                    background: jscolor.toHEXString()
                }
            }
        }
    });
}

/**
* Change the global node hover color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeHoverColor(jscolor) {
    graph.setOptions({
        nodes: {
            color: {
                hover: {
                    background: jscolor.toHEXString()
                }
            }
        }
    });
}

/**
* Change the global node hover color defined in the graph's "options"
* Object.
*
* This method is directly called from the corresponding jscolor
* component when a color is selected.
*
* @param {jscolor} jscolor the jscolor Object that represents the color
*   picker.
*
* @returns {void} nothing.
*/
function changeGlobalNodeShadowColor(jscolor) {
    if($('#gnod-shadow').prop('checked')) {
        var alpha = $('#gnod-shadow-alpha').slider('value');
        var color = jscolor.toRGBString();

        color = color.replace("rgb", "rgba");
        color = color.replace(")", "," + (alpha / 100).toString() + ")");

        graph.setOptions({
            nodes: {
                shadow: {
                    color: color,
                    size: parseInt($('#gnod-shadow-size').val()),
                    x: parseInt($('#gnod-shadow-x').val()),
                    y: parseInt($('#gnod-shadow-y').val())
                }
            }
        });
    }
}

/**
* Clear the selection of nodes/edges made by the user when an empty
* space of the graph is clicked.
*
* @param {Object} event the event fired by the graph's canvas when the user
*   clicks over it.
*
* @return {void} nothing.
*/
function clearSelection(event) {
    if(event.nodes.length === 0) {
        $('#mnod-id').val('');
        $('#mnod-label').val('');
        $('#mnod-label').attr('placeholder', 'Node label');
        document.getElementById('mnod-color').jscolor.fromString('#D2E5FF');
        multNode = false;
    }

    if(event.edges.length === 0) {
        $('#medg-id').val('');
        $('#medg-from').val('');
        $('#medg-from').attr("'From' node ID");
        $('#medg-to').val('');
        $('#medg-to').attr("'To' node ID");
        multEdge = false;
    }
}

/**
* Create the Network object that represents the graph.
*
* This method also shows the graph in the drawing area.
*
* @returns {void} nothing.
*/
function createNetwork() {
    reset();

    buildOptions();

    // Create the data for the graph
    data = {
        nodes: nodes,
        edges: edges
    }

    // Create the graph.
    graph = new vis.Network(canvas, data, options);

    // Add the manipulation to the graph
    graph.on('selectNode', function(params) {
        loadNodeData(params);
    });
    
    graph.on('selectEdge', function(params) {
        loadEdgeData(params);
    });

    graph.on('click', function(params) {
        clearSelection(params);
    });
}

/**
* Create a Neighbor-Subgraph from the selected vertex.
*
* A 'neighbor-subgraph' is a subgraph where the subset of nodes U is
* the neighborhood of a selected vertex (that is, the set of vertices
* adjacent to the selected vertex). The selected vertex will NOT BE
* included in the resulting subgraph. If more than one node is selected
* when this action is called, only the first vertex of the selection
* will be used to define the subgraph.
*
* @returns {void} nothing.
*/
function createNeighborSubgraph() {
    var selection = $('#mnod-id').val().split(',');
    var selected = nodes.get(parseInt(selection[0]));

    // Searches the neighborhood
    var neighborhood = new Set();

    var edgesIds = edges.getIds();
    var edge = null;
    
    for(var i = 0; i < edgesIds.length; i++) {
        edge = edges.get(edgesIds[i]);
        if(edge.from === selected.id || edge.to === selected.id)
            neighborhood.add(edge.from === selected.id ? edge.to : edge.from);
    }

    var subIds = "";
    var neighArray = Array.from(neighborhood);

    for(var i = 0; i < neighArray.length; i++) {
        subIds += neighArray[i].toString();
        subIds += (i !== (neighArray.length - 1) ? ',' : '');
    }

    $('#mnod-id').val(subIds);
    createSubgraph();
}

/**
* Create subgraph from the selected nodes.
*
* A subgraph of a graph G = (V, E) is a graph H = (U, F) where U is a
* subset of V, and F is a set of edges of the form:
*
*    F = {(x,y) | (x,y) belongs to E, x belongs to U, y belongs to U}
*
* All the nodes that are not selected (and the remaining edges) are
* permanently deleted from the graph.
*
* @returns {void} nothing.
*/
function createSubgraph() {
    var selectedNodes = $('#mnod-id').val().split(',');

    if(nodes.length !== 0) {
        var u = new Set(selectedNodes);

        // First delete all the non-included edges
        var edgesIds = edges.getIds();
        var edge = null;
        
        for(var i = 0; i < edgesIds.length; i++) {
            edge = edges.get(edgesIds[i]);

            if(!u.has(edge.from.toString()) || !u.has(edge.to.toString()))
                edges.remove(edge.id);
        }

        // Next delete all the non-included nodes
        var nodesIds = nodes.getIds();
        var node = null;

        for(var i = 0; i < nodesIds.length; i++) {
            node = nodes.get(nodesIds[i]);
            
            if(!u.has(node.id.toString()))
                nodes.remove(node.id);
        }
    }
}

/**
* Delete an edge from the graph.
*
* The edge is deleted from both the graph AND the edge dataset. The
* canvas is updated automatically, so no further steps are needed.
*
* @returns {void} nothing.
*/
function deleteEdge() {
    var edge = edges.get($('#medg-id').val());
    
    if(edge != null)
        if(confirm("Are you sure you wish to delete this edge? This action cannot be undone."))
            edges.remove(edge.id);
}

/**
* Delete the neighborhood of the selected vertex.
*
* The edges of the neighborhood with the remaining vertices of the 
* graph are also removed. If no vertex is selected, then no changes
* are made to the graph.
*
* @returns {void} nothing.
*/
function deleteNeighbors() {
    // Check if at least one node is selected
    var ids = $('#mnod-id').val();
    
    if(ids !== '' && ids !== ' ') {
        // If more than one vertex is selected, only the first one is
        // considered.
        var nodeIds = ids.split(',');
        var nid = parseInt(nodeIds[0]);
    
        // First, we get the neighborhood
        var neighborEdges = $('#medg-id').val().split(',');
        var neighborhood = new Set();
        var edge = null;
    
        for(var i = 0; i < neighborEdges.length; i++) {
            edge = edges.get(neighborEdges[i]);
            if(edge.from === nid)
                neighborhood.add(edge.to)
            else if(edge.to === nid)
                neighborhood.add(edge.from)
        }
        
        // Now delete all neighbor's edges
        var edgesIds = edges.getIds();
        
        for(var i = 0; i < edgesIds.length; i++) {
            edge = edges.get(edgesIds[i]);
            if(neighborhood.has(edge.from) || neighborhood.has(edge.to))
                edges.remove(edgesIds[i]);
        }
        
        // Finally, delete all the neighbors
        var neighbors = Array.from(neighborhood);
        for(var i = 0; i < neighbors.length; i++) 
            nodes.remove(parseInt(neighbors[i]));
    }
}

/**
* Delete a node from the graph.
*
* The node is deleted from both the graph AND the node dataset. The
* adjacent edges to the node are also deleted. The canvas is updated
* automatically, so no further steps are needed.
*
* @returns {void} nothing.
*/
function deleteNode() {
    if(multNode) {
        var ids = $('#mnod-id').val().split(',');
        
        if(confirm("Are you sure you wish to delete " + ids.length + " nodes? This action cannot be undone.")) {
            var edgesIds = $('#medg-id').val().split(',');

            for(var i = 0; i < edgesIds.length; i++)
                edges.remove(edgesIds[i]);
            for(var i = 0; i < ids.length; i++)
                nodes.remove(parseInt(ids[i]));
        }
    } else {
        var node = nodes.get(parseInt($('#mnod-id').val()));
    
        if(node != null)
            if(confirm("Are you sure you wish to delete this node? This action cannot be undone.")) {
                var edgesIds = $('#medg-id').val().split(',');

                for(var i = 0; i < edgesIds.length; i++)
                    edges.remove(edgesIds[i]);
            
                nodes.remove(node.id);
            }
    }
}

/**
* Fill the 'Modify edge' form with the data from a selected edge.
*
* This method is called whenever an edge of the graph is selected by the
* user.
*
* @param {Object} event the Object passed by the "click" event of the
*   Network.
*
* @returns {void} nothing.
*/
function loadEdgeData(event) {
    if(event.edges.length > 1)
        multEdge = true;
    else
        multEdge = false;

    if(multEdge) {
        var selectedIds = '';

        for(var i = 0; i < event.edges.length; i++) {
            selectedIds += edges.get(event.edges[i]).id.toString();
            selectedIds += (i !== (event.edges.length - 1) ? ',' : '');
        }

        $('#medg-id').val(selectedIds);
        $('#medg-from').val('');
        $('#medg-from').attr('placeholder', '<Multiple from nodes>');
        $('#medg-to').val('');
        $('#medg-to').attr('placeholder', '<Multiple to nodes>');
    } else {
        var selectedEdge = edges.get(event.edges[0]);

        $('#medg-id').val(selectedEdge.id);
        $('#medg-from').val(selectedEdge.from);
        $('#medg-to').val(selectedEdge.to);
    }
}

/**
* Fill the 'Modify node' form with the data from a selected node.
*
* This method is called whenever a node of the graph is selected by the
* user.
*
* @param {Object} event the Object passed by the "click" event of the 
*   Network.
*
* @returns {void} nothing.
*/
function loadNodeData(event) {
    if(event.nodes.length > 1)
        multNode = true;
    else
        multNode = false;

    if(multNode) {
        var selectedIds = '';

        for(var i = 0; i < event.nodes.length; i++) {
            selectedIds += nodes.get(event.nodes[i]).id.toString();
            selectedIds += (i !== (event.nodes.length - 1) ? ',' : '');
        }

        $('#mnod-id').val(selectedIds);
        $('#mnod-label').val('');
        $('#mnod-label').attr('placeholder', '<Multiple labels>');
        document.getElementById('mnod-color').jscolor.fromString("#D2E5FF");
    } else {
        var selectedNode = nodes.get(event.nodes[0]);

        $('#mnod-id').val(selectedNode.id);
        $('#mnod-label').val(selectedNode.label);
        if(selectedNode.color === undefined)
            selectedNode.color = "#D2E5FF";
        document.getElementById('mnod-color').jscolor.fromString(
          selectedNode.color
        );
    }

}

/**
* Update the data from an edge of the graph.
*
* The drawing of the graph is automatically updated when the edge is
* saved, so no further steps are needed.
*
* @returns {void} nothing.
*/
function modifyEdge() {
    var edge = null;

    if(multEdge) {
        var ids = $('#medg-id').val().split(',');
        var from = $('#medg-from').val();
        var to = $('#medg-to').val();
        
        for(var i = 0; i < ids.length; i++) {
            edge = edges.get(ids[i]);
            // If edge is null, the given ID is invalid
            if(edge != null) {
                edge.from = (from !== '' && from !== ' ') ? parseInt(from) : edge.from;
                edge.to = (to !== '' && to !== ' ') ? parseInt(to) : edge.to;

                edges.update(edge);
            }
        }
    } else {
        edge = edges.get($('#medg-id').val());
        // If edge is null, the given ID is invalid.
        if(edge != null) {
            edge.from = parseInt($('#medg-from').val());
            edge.to = parseInt($('#medg-to').val());

            edges.update(edge);
        }
    }
}

/**
* Update the data from a node of the graph.
*
* The drawing of the graph is automatically updated when the node is
* saved, so no further steps are needed.
*
* @returns {void} nothing.
*/
function modifyNode() {
    var picker = document.getElementById('mnod-color').jscolor;
    var node = null;
    
    if(multNode) {
        var ids = $('#mnod-id').val().split(',');
        var label = $('#mnod-label').val();
        
        for(var i = 0; i < ids.length; i++) {
            node = nodes.get(parseInt(ids[i]));
            node.label = (label !== '' && label !== ' ' ? label : node.label);
            node.color = picker.toHEXString();

            nodes.update(node);
        }
    } else {
        node = nodes.get($('#mnod-id').val());
        
        // If node is null, the given ID is invalid.
        if(node !== null) {
            node.label = $('#mnod-label').val();
            node.color = picker.toHEXString();

            nodes.update(node);
        }
    }
}

/**
* Open a file containing the definition of a graph in the DIMACS format.
*
* The DIMACS (Center of Discrete Mathematics and Theoretical Computer
* Science) defined a standard format to define graphs that is widely
* used to distribute graphs among computer scientists. You can read the
* specification of the format in the following web address:
*
* http://mat.gsia.cmu.edu/COLOR/general/ccformat.ps
*
* @param {Object} event the Event object triggered by the file chooser
*   input.
*
* @returns {void} nothing.
*/
function openDIMACS(event) {
    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function(){ parseDIMACS(reader.result) };
    reader.readAsText(file);
}

/**
* Open a file containing the definition of a graph in JSON format.
*
* The structure of the JSON object is the same defined by the Java
* Graph Viewer Engine, and it is presented as follows:
*
* {
*   "vertices" : [
*     {
*       "vid" : << Vertex ID (int) >> ,
*       "label" : << Vertex color class (String) >> ,
*       "neighbors" : [ << Neighbors Vertex IDs (ints) >> ]
*     } , ...
*   ] ,
*
*   "edges" : [
*     {
*       "endpoints" : [ << Vertex ID (int) >>, <<Vertex ID (int) >> ] ,
*       "directed" : << false | true >>
*     } , ...
*   ]
* }
*
* @param {Object} event the Event object triggered by the file chooser 
*   input.
*
* @returns {void} nothing.
*/
function openJSON(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    
    reader.onload = function() { parseJSON(reader.result) };
    reader.readAsText(file);
}

/**
* Parse a string containing the definition of a graph in the DIMACS
* standard format.
*
* This method also draws the readed graph in the canvas.
*
* @param {String} text the definition of the graph, written in the
* DIMACS format. This is usually the data readed from an input file.
*
* @returns {void} nothing.
*/
function parseDIMACS(text) {
    // Re-creates the data containers.
    nodes = new vis.DataSet();
    edges = new vis.DataSet();

    var lines = text.split("\n");
    var components = null;
    var numNodes = lines.length;

    // Process the input file
    for(var i = 0; i < numNodes; i++) {
        components = lines[i].split(" ");

        // The problem definition starts with 'p'.
        if(components[0] === "p") {
            // Create the nodes of the graph.
            var num_nodes = parseInt(components[2]);

            for(var j = 1; j <= num_nodes; j++)
                nodes.add({
                    id: j,
                    label: j.toString()
                });
        }

        // Edge definitions starts with 'e'.
        if(components[0] === "e") {
            var u = parseInt(components[1]);
            var w = parseInt(components[2]);

            edges.add({from: u, to: w});
        }

        // All other lines are ignored by now.
    }

    // Create and show the graph
    createNetwork();
}

/**
* Parse a string containing the definition of a graph in JSON format.
*
* This method also draws the parsed graph in the canvas.
*
* @param {String} text the definition of the graph, written in JSON 
*   format. This is usually the data readed from an input file.
*
* returns {void} nothing.
*/
function parseJSON(text) {
    // Re-creates the data containers.
    nodes = new vis.DataSet();
    edges = new vis.DataSet();
    
    // List of color classes
    var colors = {};
    
    // Parses the JSON text
    var json_graph = JSON.parse(text);
    
    // Recreate the vertices
    for(var i = 0; i < json_graph.vertices.length; i++) {
        var color_class = json_graph.vertices[i].label.toString();
    
        if(colors[color_class] === undefined) {
            colors[color_class] = "rgba(" 
              + (Math.floor((Math.random() * 255) + 1)).toString() + "," 
              + (Math.floor((Math.random() * 255) + 1)).toString() + ","
              + (Math.floor((Math.random() * 255) + 1)).toString() + ",255)";
        }
    
        nodes.add({
            id: json_graph.vertices[i].vid,
            label: json_graph.vertices[i].vid.toString(),
            color: colors[color_class]
        });
    }
    
    // Recreate the edges
    for(var i = 0; i < json_graph.edges.length; i++) {
        edges.add({
            from: parseInt(json_graph.edges[i].endpoints[0]),
            to: parseInt(json_graph.edges[i].endpoints[1])
        });
    }
    
    // Create and show the network
    createNetwork();
}

/**
* Reset the application to the default state.
*
* This method fills all options with the default values provided by the
* vis library.
*
* @returns {void} nothing.
*/
function reset() {
    var picker = null;

    // Global node appearance options
    $('#gnod-shape').val('ellipse');
    $('#gnod-lblsize').hide();
    $('#gnod-size').val(25).hide();
    $('#gnod-hidden').prop('checked', false);
    
    // Global node border options
    $('#gnod-border-width').val(1);
    $('#gnod-border-swidth').val(2);
    $('#gnod-border-radius').val(6);
    $('#gnod-border-dashes').prop('checked', false);
    
    picker = document.getElementById('gnod-border-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('2b7ce9');
    picker = document.getElementById('gnod-border-hcolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('2b7ce9');
    picker = document.getElementById('gnod-border-scolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('2b7ce9');
        
    // Global node color options
    picker = document.getElementById('gnod-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('97c2fc');
    picker = document.getElementById('gnod-hcolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('d2e5ff');
    picker = document.getElementById('gnod-scolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('d2e5ff');
        
    // Global node font options
    $('#gnod-font-face').val('5');
    $('#gnod-font-size').val(14);
    $('#gnod-font-sbold').prop('checked', true);
    $('#gnod-font-bg').prop('checked', false);
    $('#gnod-font-lblbgcolor').hide();
    $('#gnod-font-bgcolor').hide();
    $('#gnod-font-stroke').prop('checked', false);
    $('#gnod-font-lblskwidth').hide();
    $('#gnod-font-skwidth').val(0).hide();
    $('#gnod-font-lblskcolor').hide();
    $('#gnod-font-skcolor').hide();
    
    picker = document.getElementById('gnod-font-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('343434');
    picker = document.getElementById('gnod-font-bgcolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('ffffff');
    picker = document.getElementById('gnod-font-skcolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('ffffff');
    
    // Global node physics options
    $('#gnod-physics').prop('checked', false);
    $('#gnod-mass').val(1);
    $('#gnod-fixed').prop('checked', false);
    $('#gnod-fixed-lblx').hide();
    $('#gnod-fixed-x').prop('checked', false).hide();
    $('#gnod-fixed-lbly').hide();
    $('#gnod-fixed-y').prop('checked', false).hide();
    
    // Global node shadow options
    $('#gnod-shadow').prop('checked', false);
    $('#gnod-shadow-lblcolor').hide();
    $('#gnod-shadow-color').hide();
    $('#gnod-shadow-lblalpha').hide();
    $('#gnod-shadow-alpha').slider('value', 55).hide();
    $('#gnod-shadow-lblsize').hide();
    $('#gnod-shadow-size').val(10).hide();
    $('#gnod-shadow-lblx').hide();
    $('#gnod-shadow-x').val(5).hide();
    $('#gnod-shadow-lbly').hide();
    $('#gnod-shadow-y').val(5).hide();
    
    picker = document.getElementById('gnod-shadow-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('000000');

    // Global edge appearance options
    $('#gedg-dashes').prop('checked', false);
    $('#gedg-hidden').prop('checked', false);
    $('#gedg-physics').prop('checked', false);
    $('#gedg-width').val(1);
    
    // Global edge arrow options
    $('#gedg-arrows-to').prop('checked', false);
    $('#gedg-arrows-lbltscale').hide();
    $('#gedg-arrows-tscale').val(1).hide();
    $('#gedg-arrows-middle').prop('checked', false);
    $('#gedg-arrows-lblmscale').hide();
    $('#gedg-arrows-mscale').val(1).hide();
    $('#gedg-arrows-from').prop('checked', false);
    $('#gedg-arrows-lblfscale').hide();
    $('#gedg-arrows-fscale').val(1).hide();
    $('#gedg-arrows-strikethrough').prop('checked', true);

    // Global edge color arrows
    $('#gedg-icolor').val('from');
    $('#gedg-lblcolor').hide();
    $('#gedg-color').hide();
    $('#gedg-lblhcolor').hide();
    $('#gedg-hcolor').hide();
    $('#gedg-lblscolor').hide();
    $('#gedg-scolor').hide();
    $('#gedg-acolor').slider('value', 50);
    
    picker = document.getElementById('gedg-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('848484');
    picker = document.getElementById('gedg-hcolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('848484');
    picker = document.getElementById('gedg-scolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('848484');

    // Global edge font options
    $('#gedg-font-face').val('5');
    $('#gedg-font-size').val(14);
    $('#gedg-font-sbold').prop('checked', true);
    $('#gedg-font-bg').prop('checked', false);
    $('#gedg-font-lblbgcolor').hide();
    $('#gedg-font-bgcolor').hide();
    $('#gedg-font-stroke').prop('checked', false);
    $('#gedg-font-lblskwidth').hide();
    $('#gedg-font-skwidth').val(0).hide();
    $('#gedg-font-lblskcolor').hide();
    $('#gedg-font-skcolor').hide();
    
    picker = document.getElementById('gedg-font-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('343434');
    picker = document.getElementById('gedg-font-bgcolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('ffffff');
    picker = document.getElementById('gedg-font-skcolor');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('ffffff');
        
    // Global edge shadow options
    $('#gedg-shadow').prop('checked', false);
    $('#gedg-shadow-lblcolor').hide();
    $('#gedg-shadow-color').hide();
    $('#gedg-shadow-lblalpha').hide();
    $('#gedg-shadow-alpha').slider('value', 50).hide();
    $('#gedg-shadow-lblsize').hide();
    $('#gedg-shadow-size').val(10).hide();
    $('#gedg-shadow-lblx').hide();
    $('#gedg-shadow-x').val(5).hide();
    $('#gedg-shadow-lbly').hide();
    $('#gedg-shadow-y').val(5).hide();
    
    picker = document.getElementById('gedg-shadow-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('000000');
        
    // Global edge smoothness options
    $('#gedg-smooth').prop('checked', false);
    $('#gedg-smooth-lbltype').hide();
    $('#gedg-smooth-type').val('dynamic').hide();
    $('#gedg-smooth-lblforcedir').hide();
    $('#gedg-smooth-forcedir').val('none').hide();
    $('#gedg-smooth-lblroundness').hide();
    $('#gedg-smooth-roundness').slider('value', 50).hide();
    
    $('#anod-id').val('');
    $('#anod-label').val('');
    picker = document.getElementById('anod-color');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString("D2E5FF");

    $('#aedg-from').val('');
    $('#aedg-to').val('');

    $('#mnod-id').val('');
    $('#mnod-label').val('');
    if(picker.jscolor !== undefined)
        picker.jscolor.fromString('D2E5FF');

    $('#medg-id').val('');
    $('#medg-from').val('');
    $('#medg-to').val('');
}
