import sys

ALPHABET = [' ', 'ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'თ', 'ი', 'კ', 'ლ', 'მ', 'ნ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ', 'უ',
            'ფ', 'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ', 'წ', 'ჭ', 'ხ', 'ჯ', 'ჰ']

PAIRS = ["  ", " ა", " ბ", " გ", " დ", " ე", " ვ", " ზ", " თ", " ი", " კ", " ლ", " მ", " ნ", " ო", " პ", " ჟ", " რ",
         " ს", " ტ", " უ", " ფ", " ქ", " ღ", " ყ", " შ", " ჩ", " ც", " ძ", " წ", " ჭ", " ხ", " ჯ", " ჰ", "ა ", "აა",
         "აბ", "აგ", "ად", "აე", "ავ", "აზ", "ათ", "აი", "აკ", "ალ", "ამ", "ან", "აო", "აპ", "აჟ", "არ", "ას", "ატ",
         "აუ", "აფ", "აქ", "აღ", "აყ", "აშ", "აჩ", "აც", "აძ", "აწ", "აჭ", "ახ", "აჯ", "აჰ", "ბ ", "ბა", "ბბ", "ბგ",
         "ბდ", "ბე", "ბვ", "ბზ", "ბთ", "ბი", "ბკ", "ბლ", "ბმ", "ბნ", "ბო", "ბპ", "ბჟ", "ბრ", "ბს", "ბტ", "ბუ", "ბფ",
         "ბქ", "ბღ", "ბყ", "ბშ", "ბჩ", "ბც", "ბძ", "ბწ", "ბჭ", "ბხ", "ბჯ", "ბჰ", "გ ", "გა", "გბ", "გგ", "გდ", "გე",
         "გვ", "გზ", "გთ", "გი", "გკ", "გლ", "გმ", "გნ", "გო", "გპ", "გჟ", "გრ", "გს", "გტ", "გუ", "გფ", "გქ", "გღ",
         "გყ", "გშ", "გჩ", "გც", "გძ", "გწ", "გჭ", "გხ", "გჯ", "გჰ", "დ ", "და", "დბ", "დგ", "დდ", "დე", "დვ", "დზ",
         "დთ", "დი", "დკ", "დლ", "დმ", "დნ", "დო", "დპ", "დჟ", "დრ", "დს", "დტ", "დუ", "დფ", "დქ", "დღ", "დყ", "დშ",
         "დჩ", "დც", "დძ", "დწ", "დჭ", "დხ", "დჯ", "დჰ", "ე ", "ეა", "ებ", "ეგ", "ედ", "ეე", "ევ", "ეზ", "ეთ", "ეი",
         "ეკ", "ელ", "ემ", "ენ", "ეო", "ეპ", "ეჟ", "ერ", "ეს", "ეტ", "ეუ", "ეფ", "ექ", "ეღ", "ეყ", "ეშ", "ეჩ", "ეც",
         "ეძ", "ეწ", "ეჭ", "ეხ", "ეჯ", "ეჰ", "ვ ", "ვა", "ვბ", "ვგ", "ვდ", "ვე", "ვვ", "ვზ", "ვთ", "ვი", "ვკ", "ვლ",
         "ვმ", "ვნ", "ვო", "ვპ", "ვჟ", "ვრ", "ვს", "ვტ", "ვუ", "ვფ", "ვქ", "ვღ", "ვყ", "ვშ", "ვჩ", "ვც", "ვძ", "ვწ",
         "ვჭ", "ვხ", "ვჯ", "ვჰ", "ზ ", "ზა", "ზბ", "ზგ", "ზდ", "ზე", "ზვ", "ზზ", "ზთ", "ზი", "ზკ", "ზლ", "ზმ", "ზნ",
         "ზო", "ზპ", "ზჟ", "ზრ", "ზს", "ზტ", "ზუ", "ზფ", "ზქ", "ზღ", "ზყ", "ზშ", "ზჩ", "ზც", "ზძ", "ზწ", "ზჭ", "ზხ",
         "ზჯ", "ზჰ", "თ ", "თა", "თბ", "თგ", "თდ", "თე", "თვ", "თზ", "თთ", "თი", "თკ", "თლ", "თმ", "თნ", "თო", "თპ",
         "თჟ", "თრ", "თს", "თტ", "თუ", "თფ", "თქ", "თღ", "თყ", "თშ", "თჩ", "თც", "თძ", "თწ", "თჭ", "თხ", "თჯ", "თჰ",
         "ი ", "ია", "იბ", "იგ", "იდ", "იე", "ივ", "იზ", "ით", "იი", "იკ", "ილ", "იმ", "ინ", "იო", "იპ", "იჟ", "ირ",
         "ის", "იტ", "იუ", "იფ", "იქ", "იღ", "იყ", "იშ", "იჩ", "იც", "იძ", "იწ", "იჭ", "იხ", "იჯ", "იჰ", "კ ", "კა",
         "კბ", "კგ", "კდ", "კე", "კვ", "კზ", "კთ", "კი", "კკ", "კლ", "კმ", "კნ", "კო", "კპ", "კჟ", "კრ", "კს", "კტ",
         "კუ", "კფ", "კქ", "კღ", "კყ", "კშ", "კჩ", "კც", "კძ", "კწ", "კჭ", "კხ", "კჯ", "კჰ", "ლ ", "ლა", "ლბ", "ლგ",
         "ლდ", "ლე", "ლვ", "ლზ", "ლთ", "ლი", "ლკ", "ლლ", "ლმ", "ლნ", "ლო", "ლპ", "ლჟ", "ლრ", "ლს", "ლტ", "ლუ", "ლფ",
         "ლქ", "ლღ", "ლყ", "ლშ", "ლჩ", "ლც", "ლძ", "ლწ", "ლჭ", "ლხ", "ლჯ", "ლჰ", "მ ", "მა", "მბ", "მგ", "მდ", "მე",
         "მვ", "მზ", "მთ", "მი", "მკ", "მლ", "მმ", "მნ", "მო", "მპ", "მჟ", "მრ", "მს", "მტ", "მუ", "მფ", "მქ", "მღ",
         "მყ", "მშ", "მჩ", "მც", "მძ", "მწ", "მჭ", "მხ", "მჯ", "მჰ", "ნ ", "ნა", "ნბ", "ნგ", "ნდ", "ნე", "ნვ", "ნზ",
         "ნთ", "ნი", "ნკ", "ნლ", "ნმ", "ნნ", "ნო", "ნპ", "ნჟ", "ნრ", "ნს", "ნტ", "ნუ", "ნფ", "ნქ", "ნღ", "ნყ", "ნშ",
         "ნჩ", "ნც", "ნძ", "ნწ", "ნჭ", "ნხ", "ნჯ", "ნჰ", "ო ", "ოა", "ობ", "ოგ", "ოდ", "ოე", "ოვ", "ოზ", "ოთ", "ოი",
         "ოკ", "ოლ", "ომ", "ონ", "ოო", "ოპ", "ოჟ", "ორ", "ოს", "ოტ", "ოუ", "ოფ", "ოქ", "ოღ", "ოყ", "ოშ", "ოჩ", "ოც",
         "ოძ", "ოწ", "ოჭ", "ოხ", "ოჯ", "ოჰ", "პ ", "პა", "პბ", "პგ", "პდ", "პე", "პვ", "პზ", "პთ", "პი", "პკ", "პლ",
         "პმ", "პნ", "პო", "პპ", "პჟ", "პრ", "პს", "პტ", "პუ", "პფ", "პქ", "პღ", "პყ", "პშ", "პჩ", "პც", "პძ", "პწ",
         "პჭ", "პხ", "პჯ", "პჰ", "ჟ ", "ჟა", "ჟბ", "ჟგ", "ჟდ", "ჟე", "ჟვ", "ჟზ", "ჟთ", "ჟი", "ჟკ", "ჟლ", "ჟმ", "ჟნ",
         "ჟო", "ჟპ", "ჟჟ", "ჟრ", "ჟს", "ჟტ", "ჟუ", "ჟფ", "ჟქ", "ჟღ", "ჟყ", "ჟშ", "ჟჩ", "ჟც", "ჟძ", "ჟწ", "ჟჭ", "ჟხ",
         "ჟჯ", "ჟჰ", "რ ", "რა", "რბ", "რგ", "რდ", "რე", "რვ", "რზ", "რთ", "რი", "რკ", "რლ", "რმ", "რნ", "რო", "რპ",
         "რჟ", "რრ", "რს", "რტ", "რუ", "რფ", "რქ", "რღ", "რყ", "რშ", "რჩ", "რც", "რძ", "რწ", "რჭ", "რხ", "რჯ", "რჰ",
         "ს ", "სა", "სბ", "სგ", "სდ", "სე", "სვ", "სზ", "სთ", "სი", "სკ", "სლ", "სმ", "სნ", "სო", "სპ", "სჟ", "სრ",
         "სს", "სტ", "სუ", "სფ", "სქ", "სღ", "სყ", "სშ", "სჩ", "სც", "სძ", "სწ", "სჭ", "სხ", "სჯ", "სჰ", "ტ ", "ტა",
         "ტბ", "ტგ", "ტდ", "ტე", "ტვ", "ტზ", "ტთ", "ტი", "ტკ", "ტლ", "ტმ", "ტნ", "ტო", "ტპ", "ტჟ", "ტრ", "ტს", "ტტ",
         "ტუ", "ტფ", "ტქ", "ტღ", "ტყ", "ტშ", "ტჩ", "ტც", "ტძ", "ტწ", "ტჭ", "ტხ", "ტჯ", "ტჰ", "უ ", "უა", "უბ", "უგ",
         "უდ", "უე", "უვ", "უზ", "უთ", "უი", "უკ", "ულ", "უმ", "უნ", "უო", "უპ", "უჟ", "ურ", "უს", "უტ", "უუ", "უფ",
         "უქ", "უღ", "უყ", "უშ", "უჩ", "უც", "უძ", "უწ", "უჭ", "უხ", "უჯ", "უჰ", "ფ ", "ფა", "ფბ", "ფგ", "ფდ", "ფე",
         "ფვ", "ფზ", "ფთ", "ფი", "ფკ", "ფლ", "ფმ", "ფნ", "ფო", "ფპ", "ფჟ", "ფრ", "ფს", "ფტ", "ფუ", "ფფ", "ფქ", "ფღ",
         "ფყ", "ფშ", "ფჩ", "ფც", "ფძ", "ფწ", "ფჭ", "ფხ", "ფჯ", "ფჰ", "ქ ", "ქა", "ქბ", "ქგ", "ქდ", "ქე", "ქვ", "ქზ",
         "ქთ", "ქი", "ქკ", "ქლ", "ქმ", "ქნ", "ქო", "ქპ", "ქჟ", "ქრ", "ქს", "ქტ", "ქუ", "ქფ", "ქქ", "ქღ", "ქყ", "ქშ",
         "ქჩ", "ქც", "ქძ", "ქწ", "ქჭ", "ქხ", "ქჯ", "ქჰ", "ღ ", "ღა", "ღბ", "ღგ", "ღდ", "ღე", "ღვ", "ღზ", "ღთ", "ღი",
         "ღკ", "ღლ", "ღმ", "ღნ", "ღო", "ღპ", "ღჟ", "ღრ", "ღს", "ღტ", "ღუ", "ღფ", "ღქ", "ღღ", "ღყ", "ღშ", "ღჩ", "ღც",
         "ღძ", "ღწ", "ღჭ", "ღხ", "ღჯ", "ღჰ", "ყ ", "ყა", "ყბ", "ყგ", "ყდ", "ყე", "ყვ", "ყზ", "ყთ", "ყი", "ყკ", "ყლ",
         "ყმ", "ყნ", "ყო", "ყპ", "ყჟ", "ყრ", "ყს", "ყტ", "ყუ", "ყფ", "ყქ", "ყღ", "ყყ", "ყშ", "ყჩ", "ყც", "ყძ", "ყწ",
         "ყჭ", "ყხ", "ყჯ", "ყჰ", "შ ", "შა", "შბ", "შგ", "შდ", "შე", "შვ", "შზ", "შთ", "ში", "შკ", "შლ", "შმ", "შნ",
         "შო", "შპ", "შჟ", "შრ", "შს", "შტ", "შუ", "შფ", "შქ", "შღ", "შყ", "შშ", "შჩ", "შც", "შძ", "შწ", "შჭ", "შხ",
         "შჯ", "შჰ", "ჩ ", "ჩა", "ჩბ", "ჩგ", "ჩდ", "ჩე", "ჩვ", "ჩზ", "ჩთ", "ჩი", "ჩკ", "ჩლ", "ჩმ", "ჩნ", "ჩო", "ჩპ",
         "ჩჟ", "ჩრ", "ჩს", "ჩტ", "ჩუ", "ჩფ", "ჩქ", "ჩღ", "ჩყ", "ჩშ", "ჩჩ", "ჩც", "ჩძ", "ჩწ", "ჩჭ", "ჩხ", "ჩჯ", "ჩჰ",
         "ც ", "ცა", "ცბ", "ცგ", "ცდ", "ცე", "ცვ", "ცზ", "ცთ", "ცი", "ცკ", "ცლ", "ცმ", "ცნ", "ცო", "ცპ", "ცჟ", "ცრ",
         "ცს", "ცტ", "ცუ", "ცფ", "ცქ", "ცღ", "ცყ", "ცშ", "ცჩ", "ცც", "ცძ", "ცწ", "ცჭ", "ცხ", "ცჯ", "ცჰ", "ძ ", "ძა",
         "ძბ", "ძგ", "ძდ", "ძე", "ძვ", "ძზ", "ძთ", "ძი", "ძკ", "ძლ", "ძმ", "ძნ", "ძო", "ძპ", "ძჟ", "ძრ", "ძს", "ძტ",
         "ძუ", "ძფ", "ძქ", "ძღ", "ძყ", "ძშ", "ძჩ", "ძც", "ძძ", "ძწ", "ძჭ", "ძხ", "ძჯ", "ძჰ", "წ ", "წა", "წბ", "წგ",
         "წდ", "წე", "წვ", "წზ", "წთ", "წი", "წკ", "წლ", "წმ", "წნ", "წო", "წპ", "წჟ", "წრ", "წს", "წტ", "წუ", "წფ",
         "წქ", "წღ", "წყ", "წშ", "წჩ", "წც", "წძ", "წწ", "წჭ", "წხ", "წჯ", "წჰ", "ჭ ", "ჭა", "ჭბ", "ჭგ", "ჭდ", "ჭე",
         "ჭვ", "ჭზ", "ჭთ", "ჭი", "ჭკ", "ჭლ", "ჭმ", "ჭნ", "ჭო", "ჭპ", "ჭჟ", "ჭრ", "ჭს", "ჭტ", "ჭუ", "ჭფ", "ჭქ", "ჭღ",
         "ჭყ", "ჭშ", "ჭჩ", "ჭც", "ჭძ", "ჭწ", "ჭჭ", "ჭხ", "ჭჯ", "ჭჰ", "ხ ", "ხა", "ხბ", "ხგ", "ხდ", "ხე", "ხვ", "ხზ",
         "ხთ", "ხი", "ხკ", "ხლ", "ხმ", "ხნ", "ხო", "ხპ", "ხჟ", "ხრ", "ხს", "ხტ", "ხუ", "ხფ", "ხქ", "ხღ", "ხყ", "ხშ",
         "ხჩ", "ხც", "ხძ", "ხწ", "ხჭ", "ხხ", "ხჯ", "ხჰ", "ჯ ", "ჯა", "ჯბ", "ჯგ", "ჯდ", "ჯე", "ჯვ", "ჯზ", "ჯთ", "ჯი",
         "ჯკ", "ჯლ", "ჯმ", "ჯნ", "ჯო", "ჯპ", "ჯჟ", "ჯრ", "ჯს", "ჯტ", "ჯუ", "ჯფ", "ჯქ", "ჯღ", "ჯყ", "ჯშ", "ჯჩ", "ჯც",
         "ჯძ", "ჯწ", "ჯჭ", "ჯხ", "ჯჯ", "ჯჰ", "ჰ ", "ჰა", "ჰბ", "ჰგ", "ჰდ", "ჰე", "ჰვ", "ჰზ", "ჰთ", "ჰი", "ჰკ", "ჰლ",
         "ჰმ", "ჰნ", "ჰო", "ჰპ", "ჰჟ", "ჰრ", "ჰს", "ჰტ", "ჰუ", "ჰფ", "ჰქ", "ჰღ", "ჰყ", "ჰშ", "ჰჩ", "ჰც", "ჰძ", "ჰწ",
         "ჰჭ", "ჰხ", "ჰჯ", "ჰჰ"]


class ProbabilityCounter:
    items = {}
    entryCount = 0

    def __init__(self):
        self.items = {}
        self.entryCount = 0

    def add_entry(self, entry):
        self.entryCount = self.entryCount + 1

        if entry in self.items:
            self.items[entry] = self.items[entry] + 1
        else:
            self.items[entry] = 1

    def get_probability(self, entry):
        if entry in self.items:
            return self.items[entry] / self.entryCount
        return 0

    def get_entries(self):
        return self.items.keys()


def format_probability(probability):
    return str(format(probability, '.7f'))


def process_files(file_names):
    source_file = open(file_names[0], 'r', encoding="utf8")
    dest_file = open(file_names[1], 'w', encoding="utf8")

    char_probabilities = ProbabilityCounter()
    pair_probabilities = ProbabilityCounter()

    buffer = '  '

    while True:
        curr = source_file.read(1)
        if not curr:
            break
        buffer = buffer[1:] + curr
        char_probabilities.add_entry(curr)
        pair_probabilities.add_entry(buffer)

    for char in ALPHABET:
        dest_file.write(format_probability(char_probabilities.get_probability(char)))
        dest_file.write(' ')

    dest_file.write('\n')

    for pair in PAIRS:
        dest_file.write(format_probability(pair_probabilities.get_probability(pair)))
        dest_file.write(' ')

    source_file.close()
    dest_file.close()


def main(argv):
    if len(argv) != 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
