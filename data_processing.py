import re

x = """
<div class="forix-chartjs" data-chart-background="https://www.sweetmarias.com/media/wysiwyg/Bg-Cupping-02.png" data-chart-label="Ethiopia Bensa Kebele Mirado" data-chart-id="cupping-chart" data-chart-type="radar" data-chart-value="Dry Fragrance:9.1,Wet Aroma:9.2,Brightness:9.2,Flavor:9,Body:8.5,Finish:8.6,Sweetness:9,Clean Cup:8.1,Complexity:9,Uniformity:8.5" data-chart-score="89.2" data-cupper-correction="1">
</div>
<div class="forix-chartjs" data-chart-background="https://www.sweetmarias.com/media/wysiwyg/Bg-FlavorChart-01.png" data-chart-label="Ethiopia Bensa Kebele Mirado" data-chart-id="flavor-chart" data-chart-type="polarArea" data-chart-value="Floral:2,Honey:3,Sugars:2,Caramel:0,Fruits:2,Citrus:3,Berry:0,Cocoa:0,Nuts:0,Rustic:0,Spice:1,Body:3">
</div>
    """

flavors_string = re.findall('data-chart-id="flavor-chart".*data-chart-value="(.*?)"', x)
flavors = re.findall('[A-Z].*?:[0-9]', flavors_string[0])
#print(flavors)

scores_string = re.findall('data-chart-id="cupping-chart".*data-chart-value="(.*?)"', x)
scores = re.findall('[A-Z].*?:[0-9]\.*[0-9]*', scores_string[0])
#print(scores)

for flavor in flavors:
    print(flavor.split(':'))

for score in scores:
    print(score.split(':'))