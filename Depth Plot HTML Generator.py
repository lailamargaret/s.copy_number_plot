#This script reads from cnvs files and writes to a .txt file in the format used by google charts for line graphs with tooltips 

###CLASS: Gene 
###FUNCTION: Stores information in member variables
###CONSTRUCTION: Requires strings
class Tile:    
    def __init__ (self, tile, gene, s_depth, z_score, loc, gl_depth, gl_z_score):
        self.tile = tile
        self.s_depth = s_depth
        self.z_score = z_score
        self.loc = loc
        self.gene = gene
        self.gl_depth = gl_depth
        self.gl_z_score = gl_z_score

###FUNCTION: Writes a HTML file with same name as input file + ".HTML_graph.html" 
### Lines broken up for readability of HTML
### Args: list of Tile objects, tile-level file to use for naming output file
def create_HTML(items, tl_file):
    name_parts = tl_file.split(".")
    outfile = name_parts[0] + ".HTML_graph.html"
    
    file = open(outfile, "w")

    #write to a file in HTML, separated for readability
    file.write("<html>\n<title>Interactive Heme Data</title>")
    file.write("\n<head>\n\t<script type=""text/javascript"" src=""https://www.gstatic.com/charts/loader.js""></script>")
    file.write("\n\t<script type=""text/javascript"">")
    file.write("\n\t\tgoogle.charts.load('current', {packages: ['corechart', 'line']});")
    file.write("\n\t\tgoogle.charts.setOnLoadCallback(drawChart);")
    file.write("\n\tfunction drawChart()") 
    file.write("{\n\t\tvar data = new google.visualization.DataTable();")
    #add columns to data table
    file.write("\n\t\tdata.addColumn('number', 'X');")
    file.write("\n\t\tdata.addColumn('number', 'Details');")
    file.write("\n\t\tdata.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});")
    file.write("\n\n\tdata.addRows([")
    #populate data table
    i=0
    while (i < len(items)):
        file.write("[%s, %s, createTT('%s', '%s', '%s', '%s', '%s')] , " % (items[i].loc, items[i].s_depth, items[i].tile, items[i].s_depth, items[i].z_score, items[i].gl_depth, items[i].gl_z_score))
        i += 1
    file.write("]);\n")

    file.write("\nvar options = {\n\tlegend: 'none',\n\twidth: 2000,\n\theight: 1000,\n\tAxis: {title: 'Location'},\n\tvAxis: {title: 'normalized fold-depth', ticks: [ ")
    file.write("0, 1, 2, 3, 4, 5]},\n\tcolors: ['#9A260E'],\n\ttooltip: {isHtml: true}, \n\thAxis: {gridlines: {color: 'none'}, textPosition: 'none'}, \n\tcrosshair: {trigger:'both', color: 'darkred', opacity: 0.25}};\n")
    file.write("\n\nvar chart = new google.visualization.LineChart(document.getElementById('chart_div'));") 
    file.write("\n\nchart.draw(data, options);}")

    #writes the custom tooltip function
    file.write("\n\nfunction createTT(tile, depth, z_score, gl_depth, gl_z_score){")
    file.write("\n\treturn '<div style= \"padding: 5px 5px 5px 5px;\">'+ '<table>' + ")
    file.write("\n\t'<tr>' + '<td><b>Tile</b>: '+ tile + '</td>' + '</tr>' +")
    file.write("\n\t'<tr>' + '<td><b>Depth</b>: '+ depth + '</td>' + '</tr>' +")
    file.write("\n\t'<tr>' + '<td><b>z-score</b>: '+ z_score+ '</td>' + '</tr>' +")
    file.write("\n\t'<tr>' + '<td><b>Gene-Level Depth</b>: '+ gl_depth + '</td>' + '</tr>' +")
    file.write("\n\t'<tr>' + '<td><b>Gene-Level z-score</b>: '+ gl_z_score+ '</td>' + '</tr>'+")
    file.write("\n\t'</table>' + '</div>';}")   

    file.write("\n\n</script>\n</head>\n<body>\n<style>\ndiv.google-visualization-tooltip")
    file.write("\n\t{border: solid 1px #bdbdbd;")
    file.write("\n\tborder-radius: 2px;")
    file.write("\n\tbackground-color: white;")
    file.write("\n\tposition: absolute;")
    file.write("\n\tbox-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.6);")
    file.write("\n\tfont-size: 16px;")
    file.write("\n\t-moz-box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.6);")
    file.write("\n\t-webkit-box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.6);")
    file.write("\n\tfont-family: arial;}")
    file.write("\n\n</style>\n<div id=""chart_div""></div>\n</body>\n</html>")

    file.close()

###FUNCTION: Creates a dictionary of gene-level depth information
###ARGUMENT: infile - the file of gene-level information to be read from
def gl_depth (infile):       
    gene_level_mean_depth = {}       
   
    #Populates dictionary with gene-level information
    with open(infile, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            elif line.startswith("Gene"):
                continue
            else:
                fields = line.split("\t")
                gene_level_mean_depth[fields[0]] = fields[5]
    return gene_level_mean_depth

###FUNCTION: Creates a dictionary of gene-level mean z-score information
###ARGUMENT: infile - the file of gene-level information to be read from
def gl_z_score (infile):       
    gene_level_mean_z_score = {}       
   
    #Populates dictionary with gene-level information
    with open(infile, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            elif line.startswith("Gene"):
                continue
            else:
                fields = line.split("\t")
                gene_level_mean_z_score[fields[0]] = fields[8]
    return gene_level_mean_z_score
   
###FUNCTION: Creates tile items to store all information for each data point
###ARGUMENTS: gene_level_mean_depth and gene_level_mean_z_score - from previous functions, gene-level information for each tile
###             infile - the tile-level information
def create_tile_items(gene_level_mean_depth, gene_level_mean_z_score, infile):    
    #Loops through the file, reads, writes to a list of Tile objects called items
    items = []
    with open(infile, 'r') as f:
        idx = 0
        for line in f:
            if line.startswith("Description"): #skip the header row
                continue
            fields = line.split("\t") #list of each column
            values = [] #temp array values stores the information as it is being read to later instantiate Tile objects
            tile = fields[0]
            values.append(tile) #tile
            splitDesc = tile.split("-")
            geneName = splitDesc[0]
            values.append(geneName) #gene      
            values.append(fields[10]) #s_depth
            values.append(fields[11]) #z_score
            values.append(idx) #loc
            #gene-level information lookup to construct the object with correct information
            if (geneName == "CommonSNP"):
                values.append("N/A") #gl_depth if SNP, not gene
                values.append("N/A") #gl_z_score
            else:
                values.append(gene_level_mean_depth[geneName]) #gl_depth
                values.append(gene_level_mean_z_score[geneName]) #gl_z_score
            item = Tile(*values) #Instantiates Tile items
            items.append(item) #Adds Tile tiem to the list "items"
            idx += 1
            
    return items

def main (gl_file, tl_file):
    tiles = create_tile_items(gl_depth(gl_file), gl_z_score(gl_file), tl_file)
    create_HTML(tiles, tl_file)
    
main("N:\Clinlab\Private\Molecular Pathology\mpdocs\MDX Staff Files\Laila\Depth Plot Graph Project/SampleN_HEME0028.cnvs", "N:\Clinlab\Private\Molecular Pathology\mpdocs\MDX Staff Files\Laila\Depth Plot Graph Project/SampleN_HEME0028.tiles.cnvs")

 

