from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Class 8 Jumbled Sentences with Solutions', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 12)

sentences = [
    ("called / rose / the / queen / the / is / flowers / of", "The rose is called the queen of flowers."),
    ("widely / it / grown / is / the / all / world / over", "It is widely grown all over the world."),
    ("500 / there / about / are / species / roses / of", "There are about 500 species of roses."),
    ("the / rose / Persian / best / is / the", "The Persian rose is the best."),
    ("brought / from / there / was / it / India / to", "From there it was brought to India."),
    ("person / a / Healthy / exercise / makes", "Exercise makes a person healthy."),
    ("important / in / life / it / one’s / is", "It is important in one’s life."),
    ("exercises / physical / person / make / physically / a / fit", "Physical exercises make a person physically fit."),
    ("mental / makes / fresh / the / exercise / mind", "Mental exercise makes the mind fresh."),
    ("mind / it / sharp / makes / the / too", "It makes the mind sharp too."),
    ("keep / vitamins / fit / body / our", "Vitamins keep our body fit."),
    ("appetite / they / and / improve / body’s / increase / ability / fight / to / diseases", "They improve appetite and increase body’s ability to fight diseases."),
    ("useful / camel / is / animal / desert / the / most / the / in / the", "The camel is the most useful animal in the desert.")
]

for jum, sol in sentences:
    pdf.cell(0, 10, f'Jumbled: {jum}', 0, 1)
    pdf.multi_cell(0, 10, f'Solution: {sol}', 0, 1)
    pdf.ln(2)

pdf_file = 'class_8_jumbled_sentences.pdf'
pdf.output(pdf_file)
print(f"PDF file '{pdf_file}' has been generated successfully.")
