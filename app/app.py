# Import necessary Python and Shiny modules
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins

# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

# Set up page options like title and layout behavior
ui.page_opts(title="Palmer Penguins data dashboard", fillable=True)

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
    ui.input_radio_buttons(
        "chart_type",
        "Chart Type",
        choices=["Scatterplot", "Histogram"],
        selected="Scatterplot"
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

        # ✅ FIXED: Moved render.plot inside the card
        @render.plot
        def length_depth():
            if input.chart_type() == "Histogram":
                return sns.histplot(
                    data=filtered_df(),
                    x="bill_length_mm",
                    hue="species",
                    multiple="stack",
                    kde=True
                )
            else:
                return sns.scatterplot(
                    data=filtered_df(),
                    x="bill_length_mm",
                    y="bill_depth_mm",
                    hue="species"
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

# Define a reactive expression that filters the dataset based on user input
@reactive.calc
def filtered_df():
    # Filter by selected species
    filt_df = df[df["species"].isin(input.species())]
    # Further filter by selected body mass threshold
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]

    # Drop rows with missing values needed for plotting
    filt_df = filt_df.dropna(subset=["bill_length_mm", "bill_depth_mm", "body_mass_g", "species"])
    return filt_df
