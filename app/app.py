# Import necessary Python and Shiny modules
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins
import random

# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

# Bonus: List of penguin fun facts
penguin_facts = [
    "Penguins can drink sea water — their glands filter the salt!",
    "Gentoo penguins can swim up to 22 miles per hour.",
    "Penguins huddle together to keep warm in extreme cold.",
    "Chinstrap penguins are named for the thin black line under their heads.",
    "Emperor penguins can dive deeper than 500 meters."
]


# Set up page options like title and layout behavior
ui.page_opts(title="Palmer Penguins data dashboard", fillable=True)

#  Add custom styles to improve visual appearance
ui.tags.style(
    """
    .value-box {
        background-color: #e6f2ff !important;
        color: #003366 !important;
        font-size: 1.1rem;
    }
    .card-header {
        background-color: #004080 !important;
        color: white !important;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 10px;
    }
    """
)

# Define the sidebar with interactive controls
with ui.sidebar(title="Filter Penguins Data"):
    # Slider to select the maximum body mass
    ui.input_slider("mass", "Maximum Body Mass (grams)", 2000, 6000, 6000)
    
    # Checkboxes to filter by species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # Add helpful resource links
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Create a row of value boxes showing summary statistics
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Total penguins matching filters"

        # Display the number of penguins in the filtered dataset
        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length (mm)"

        # Display the average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth (mm)"

        # Display the average bill depth
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Add plots and data tables in a column layout
with ui.layout_columns():
    with ui.card(full_screen=True):
        # Card showing scatterplot of bill length vs. depth
        ui.card_header("Bill Length vs. Bill Depth Scatterplot")

        @render.plot
        def length_depth():
            sns.set_palette("Set2")  # Custom chart colors
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        # Card showing filtered penguin data in a table
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)
         # Bonus: Fun Fact Card
    with ui.card():
        ui.card_header("Random Penguin Fun Fact")
        @render.text
        def fun_fact():
            return random.choice(penguin_facts)

# Define a reactive expression that filters the dataset based on user input
@reactive.calc
def filtered_df():
    # Filter by selected species
    filt_df = df[df["species"].isin(input.species())]
    # Further filter by selected body mass threshold
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
