"""
FracAbility has different types of data that needs to be represented in different ways. In the Plotters module
different class adapters are proposed to plot the data. It is possible to plot:


Fracture Network (entity):


1. The geopandas dataframe -> matplotlib:
    + Fractures:
        + Rose plot
        + Backbone(s) -> Different colors if multiple backbones are present
    + Boundary
    + Nodes:
        + Different colors and shapes depending on the node type

2. The VTK entities -> pyvista:
    + Fractures:
        + Backbone(s) -> Different colors if multiple backbones are present
    + Boundary
    + Nodes:
        + Different colors depending on the node type

3. The topology data -> matplotlib:
    + I,Y,X node proportions in a ternary plot

Fracture network (statistics):

1. The statistics -> matplotlib:

    + Single distribution plot (each alone or together):
        + pdf
        + cdf
        + sf
        + summary table

    + Multiple distribution plot:
        + cdf vs ecdf
        + pdf vs histograms
        + P-P and Q-Q plot?

"""
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pyvista import Plotter
import ternary
from fracability.operations.Statistics import NetworkDistribution, NetworkFitter
import numpy as np
from scipy.stats import uniform, ecdf

def matplot_nodes(entity,
                  markersize=7,
                  return_plot=False,
                  show_plot=True):
    """
    Plot a fracability Nodes entity using matplotlib.

    :param entity: Nodes entity to plot
    :param markersize: Size of the markers as int
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned

    Notes
    -------
    The nodes are represented using this color and marker codes:

    1. I nodes: blue red circle
    2. Y nodes: green triangle
    3. Y2 nodes: cyan triangle
    4. X nodes: blue square
    5. U nodes: yellow pentagon
    """

    if 'Fracture net plot' not in plt.get_figlabels():
        figure = plt.figure(num=f'Nodes plot')

        ax = plt.subplot(111)
    else:
        ax = plt.gca()
    vtk_object = entity.vtk_object
    points = vtk_object.points
    node_types = vtk_object['n_type']
    I = np.where(node_types == 1)
    Y = np.where(node_types == 3)
    X = np.where(node_types == 4)
    U = np.where(node_types == 5)
    Y2 = np.where(node_types == 6)

    ax.plot(points[I][:, 0], points[I][:, 1], 'or', markersize=markersize)
    ax.plot(points[Y][:, 0], points[Y][:, 1], '^g', markersize=markersize)
    ax.plot(points[Y2][:, 0], points[Y2][:, 1], '^c', markersize=markersize)
    ax.plot(points[X][:, 0], points[X][:, 1], 'sb', markersize=markersize)
    ax.plot(points[U][:, 0], points[U][:, 1], 'py', markersize=markersize)

    if return_plot:
        return ax
    else:
        if show_plot:
            plt.show()


def matplot_fractures(entity,
                      linewidth=1,
                      color='black',
                      color_set=False,
                      return_plot=False,
                      show_plot=True):
    """
    Plot a fracability Fracture entity using matplotlib.

    :param entity: Fracture entity to plot
    :param linewidth: Size of the lines as int
    :param color: General color of the lines as str.
    :param color_set: Bool. If true the lines are based on the set values.
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned

    """
    if 'Fracture net plot' not in plt.get_figlabels():
        figure = plt.figure(num=f'Fractures plot')

        ax = plt.subplot(111)
    else:
        ax = plt.gca()

    if color_set:
        if 'f_set' in entity.entity_df.columns:
            n_sets = len(set(entity.entity_df['f_set']))
            cmap = matplotlib.colormaps.get_cmap("rainbow").resampled(n_sets)
            entity.entity_df.plot(ax=ax,
                                  cmap=cmap,
                                  linewidth=linewidth)
        else:
            return False
    else:

        entity.entity_df.plot(ax=ax, color=color, linewidth=linewidth)

    if return_plot:
        return ax
    else:
        if show_plot:
            plt.show()


def matplot_boundaries(entity,
                       linewidth=1,
                       color='black',
                       return_plot=False,
                       show_plot=True):
    """
    Plot a fracability Boundary entity using matplotlib.

    :param entity: Boundary entity to plot
    :param linewidth: Size of the lines as int
    :param color: General color of the lines as str
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned
    """

    if 'Fracture net plot' not in plt.get_figlabels():
        figure = plt.figure(num=f'Boundaries plot')

        ax = plt.subplot(111)
    else:
        ax = plt.gca()

    entity.entity_df.plot(ax=ax, color=color, linewidth=linewidth)

    if return_plot:
        return ax
    else:
        if show_plot:
            plt.show()


def matplot_frac_net(entity,
                     markersize=5,
                     linewidth=[2, 2],
                     color=['black', 'blue'],
                     color_set=False,
                     return_plot=False,
                     show_plot=True):
    """
    Plot a fracability FractureNetwork entity using matplotlib.

    :param entity: FractureNetwork entity to plot
    :param markersize: Size of the nodes
    :param linewidth: Size of the lines as a list of ints. The first value of the list will be the width of the fractures
    while the second the width of the boundary.
    :param color: General color of the lines as list of strings. The first value of the list will be the width of the fractures
    while the second the width of the boundary.
    :param color_set: Bool. If true the lines are based on the set values.
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned

    """
    figure = plt.figure(num=f'Fracture net plot')
    ax = plt.subplot(111)
    nodes = entity.nodes
    fractures = entity.fractures
    boundary = entity.boundaries

    if fractures is not None:
        matplot_fractures(fractures, linewidth=linewidth[0], color=color[0], color_set=color_set, return_plot=True)
    if boundary is not None:
        matplot_boundaries(boundary, linewidth=linewidth[1], color=color[1], return_plot=True)
    if nodes is not None:
        matplot_nodes(nodes, markersize=markersize, return_plot=True)

    if return_plot:
        return ax
    else:
        if show_plot:
            plt.show()


def vtkplot_nodes(entity,
                  markersize=7,
                  return_plot=False,
                  show_plot=True):
    """
    Plot a fracability Nodes entity using vtk.

    :param entity: FractureNetwork entity to plot
    :param markersize: Size of the nodes
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned

    """
    plotter = Plotter()
    plotter.background_color = 'gray'
    plotter.view_xy()
    plotter.enable_image_style()

    class_dict = {
        1: 'I',
        2: 'V',
        3: 'Y',
        4: 'X',
        5: 'U',
        6: 'Y2'
    }
    cmap_dict = {
        'I': 'Blue',
        'Y': 'Green',
        'Y2': 'Cyan',
        'X': 'Red',
        'U': 'Yellow'
    }

    nodes = entity.vtk_object

    class_names = [class_dict[int(i)] for i in nodes['n_type']]

    used_tags = list(set(class_names))
    used_tags.sort()
    cmap = [cmap_dict[i] for i in used_tags]

    sargs = dict(interactive=False,
                 vertical=False,
                 height=0.1,
                 title_font_size=16,
                 label_font_size=14)

    actor = plotter.add_mesh(nodes,
                             scalars=class_names,
                             render_points_as_spheres=True,
                             point_size=markersize,
                             show_scalar_bar=True,
                             scalar_bar_args=sargs,
                             cmap=cmap)

    if return_plot:
        return actor
    else:
        if show_plot:
            plotter.reset_camera()
            plotter.show()


def vtkplot_fractures(entity,
                      linewidth=1,
                      color='white',
                      color_set=False,
                      return_plot=False,
                      show_plot=True,
                      display_property: str = None):

    """
    Plot a fracability Fracture entity using vtk.

    :param entity: Fracture entity to plot
    :param linewidth: width of the lines
    :param color: General color of the lines as str.
    :param color_set: Bool. If true the fractures are colored using the set.
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned

    """

    plotter = Plotter()
    plotter.background_color = 'gray'
    plotter.view_xy()
    plotter.enable_image_style()

    vtk_object = entity.vtk_object

    if color_set:
        display_property = 'f_set'

    if display_property:

        if display_property in vtk_object.array_names:
            n_sets = len(set(vtk_object[display_property]))
            cmap = matplotlib.colormaps.get_cmap("rainbow").resampled(n_sets)
            actor = plotter.add_mesh(entity.vtk_object, #this needs fixin'. Connecting fractures color are "contaminated"
                                     scalars=display_property,
                                     line_width=linewidth,
                                     cmap=cmap,
                                     show_scalar_bar=False)
        else:
            return False
    else:

        actor = plotter.add_mesh(entity.vtk_object,
                                 color=color,
                                 line_width=linewidth,
                                 show_scalar_bar=False)

    if return_plot:
        return actor
    else:
        if show_plot:
            plotter.reset_camera()
            plotter.show()


def vtkplot_boundaries(entity,
                       linewidth=1,
                       color='white',
                       return_plot=False,
                       show_plot=True):
    """
    Plot a fracability Boundary entity using vtk.

    :param entity: Fracture entity to plot
    :param linewidth: width of the lines
    :param color: General color of the lines as str.
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned
    """
    plotter = Plotter()
    plotter.background_color = 'gray'
    plotter.view_xy()
    plotter.enable_image_style()

    actor = plotter.add_mesh(entity.vtk_object,
                     color=color,
                     line_width=linewidth,
                     show_scalar_bar=False)

    if return_plot:
        return actor
    else:
        if show_plot:
            plotter.reset_camera()
            plotter.show()


def vtkplot_frac_net(entity,
                     markersize=5,
                     linewidth=[2, 2],
                     color=['white', 'white'],
                     color_set=False,
                     return_plot=False,
                     show_plot=True):
    """
    Plot a fracability FractureNetwork entity using matplotlib.

    :param entity: FractureNetwork entity to plot
    :param markersize: Size of the nodes
    :param linewidth: Size of the lines as a list of ints. The first value of the list will be the width of the fractures
    while the second the width of the boundary.
    :param color: General color of the lines as list of strings. The first value of the list will be the width of the fractures
    while the second the width of the boundary.
    :param color_set: Bool. If true the lines are based on the set values.
    :param return_plot: Bool. If true the plot is returned. By default, False
    :param show_plot: Bool. If true the plot is shown. By default, True
    :return: If return_plot is true a matplotlib axis is returned

    """
    plotter = Plotter()
    plotter.background_color = 'gray'
    plotter.view_xy()
    plotter.add_camera_orientation_widget()
    plotter.enable_image_style()

    nodes = entity.nodes
    fractures = entity.fractures
    boundaries = entity.boundaries

    if nodes is not None:
        node_actor = vtkplot_nodes(nodes, markersize=markersize, return_plot=True)
        plotter.add_actor(node_actor)

    if fractures is not None:
        fractures_actor = vtkplot_fractures(fractures, linewidth=linewidth[0],
                                            color=color[0], color_set=color_set, return_plot=True)
        plotter.add_actor(fractures_actor)

    if boundaries is not None:
        boundary_actor = vtkplot_boundaries(boundaries, linewidth=linewidth[1], color=color[1], return_plot=True)
        plotter.add_actor(boundary_actor)

    if return_plot:
        actors = plotter.actors
        return actors
    else:
        if show_plot:
            plotter.reset_camera()
            plotter.show()


def matplot_stats_pdf(network_distribution: NetworkDistribution,
                      histogram: bool = True,
                      show_plot: bool = True):
    """
    Plot PDF and histogram.

    Parameters
    -------
    network_distribution: Input NetworkDistribution object

    histogram: Bool. If true plot also the histogram of the data. By default, is True

    show_plot: Bool. If true show the plot. By default, is True

    """
    sns.set_theme()
    distribution = network_distribution.distribution
    name = network_distribution.distribution_name

    network_data = network_distribution.fit_data

    x_vals = network_data.lengths

    if show_plot:
        fig = plt.figure(num=f'{name} PDF plot', figsize=(13, 7))
        fig.text(0.5, 0.95, name, ha='center')

    y_vals = distribution.pdf(x_vals)

    sns.lineplot(x=x_vals, y=y_vals, color='r', label=f'{name} pdf')
    if histogram:
        sns.histplot(x_vals, stat='density')

    plt.xlabel('length [m]')
    plt.title('PDF')
    plt.grid(True)
    plt.legend()

    if show_plot:
        plt.show()


def matplot_stats_cdf(network_distribution: NetworkDistribution,
                      plot_ecdf: bool = True,
                      show_plot: bool = True):
    """
    Plot CDF and ECDF.

    Parameters
    -------
    network_distribution: Input NetworkDistribution object

    plot_ecdf: Bool. If true plot also the empirical CDF curve of the data. By default, is True

    show_plot: Bool. If true show the plot. By default, is True

    """
    sns.set_theme()

    distribution = network_distribution.distribution
    name = network_distribution.distribution_name

    network_data = network_distribution.fit_data

    x_vals = network_data.lengths

    if show_plot:
        fig = plt.figure(num=f'{name} CDF plot', figsize=(13, 7))
        fig.text(0.5, 0.95, name, ha='center')

    y_vals = distribution.cdf(x_vals)

    sns.lineplot(x=x_vals, y=y_vals, color='r', label=f'{name} CDF')
    if plot_ecdf:
        ecdf = network_data.ecdf
        sns.lineplot(x=ecdf.quantiles, y=ecdf.probabilities, color='b', label='Empirical CDF')

    plt.xlabel('length [m]')
    plt.title('CDF')
    plt.grid(True)
    plt.legend()

    if show_plot:
        plt.show()


def matplot_stats_sf(network_distribution: NetworkDistribution,
                     plot_esf: bool = True,
                     show_plot: bool = True):
    """
    Plot SF and ESF.

    Parameters
    -------
    network_distribution: Input NetworkDistribution object

    plot_esf: Bool. If true plot also the empirical SF curve of the data. By default, is True

    show_plot: Bool. If true show the plot. By default, is True

    """
    sns.set_theme()
    distribution = network_distribution.distribution
    name = network_distribution.distribution_name

    network_data = network_distribution.fit_data

    x_vals = network_data.lengths

    if show_plot:
        fig = plt.figure(num=f'{name} SF plot', figsize=(13, 7))
        fig.text(0.5, 0.95, name, ha='center')

    y_vals = distribution.sf(x_vals)

    sns.lineplot(x=x_vals, y=y_vals, color='r', label=f'{name} SF')
    if plot_esf:
        esf = network_data.esf
        sns.lineplot(x=esf.quantiles, y=esf.probabilities, color='b', label='Empirical SF')

    plt.xlabel('length [m]')
    plt.title('SF')
    plt.grid(True)
    plt.legend()

    if show_plot:
        plt.show()


def matplot_stats_table(network_distribution: NetworkDistribution,
                        vertical: bool = True,
                        show_plot: bool = True):
    """
    Plot the stats summary table for both the data and the NetworkDistribution. In particular the following
    estimators are calculated:

        1. Mean
        2. Standard Deviation
        3. Variance
        4. Median
        5. Mode
        6. 5th percentile
        7. 95th percentile
        8. Total number of fractures
        9. % censored

    Parameters
    -----------
    network_distribution: Input NetworkDistribution object

    vertical: Bool. If true the table is vertical (2cols x 7rows). By default, is True

    show_plot: Bool. If true show the plot. By default, is True

    """

    name = network_distribution.distribution_name

    if show_plot:
        fig = plt.figure(num=f'{name} summary table')
        fig.text(0.5, 0.95, f'{name} summary table', ha='center')

    network_data = network_distribution.fit_data
    plt.axis("off")
    dec = 4

    text_mean = f'{np.round(network_distribution.mean, dec)}'
    text_std = f'{np.round(network_distribution.std, dec)}'
    text_var = f'{np.round(network_distribution.var, dec)}'
    text_median = f'{np.round(network_distribution.median, dec)}'
    text_mode = f'{np.round(network_distribution.mode[0], dec)}'
    text_b5 = f'{np.round(network_distribution.b5, dec)}'
    text_b95 = f'{np.round(network_distribution.b95, dec)}'

    text_mean_th = f'{np.round(network_data.mean, dec)}'
    text_std_th = f'{np.round(network_data.std, dec)}'
    text_var_th = f'{np.round(network_data.var, dec)}'
    text_median_th = f'{np.round(network_data.median, dec)}'
    text_mode_th = f'{np.round(network_data.mode[0], dec)}'
    text_b5_th = f'{np.round(network_data.b5, dec)}'
    text_b95_th = f'{np.round(network_data.b95, dec)}'

    text_totalf = f'{network_data.total_n_fractures}'
    text_perc_censor = f'{np.round(network_data.censoring_percentage, dec)}'

    general_stats_df = pd.DataFrame(data=[[text_totalf, text_perc_censor]],
                                    columns=['Total number of fractures', '% censored'])

    stats_df = pd.DataFrame(data=[[text_mean_th, text_mean],
                                  [text_median_th, text_median],
                                  [text_mode_th, text_mode],
                                  [text_b5_th, text_b5],
                                  [text_b95_th, text_b95],
                                  [text_std_th, text_std],
                                  [text_var_th, text_var]],
                            columns=['Data', 'Fit'], index=['Mean', 'Median', 'Mode',
                                                            'B5', 'B95', 'Std', 'Var'])
    if not vertical:
        stats_df = stats_df.transpose()

    plt.table(cellText=general_stats_df.values,
              colLabels=general_stats_df.columns,
              # colWidths=[0.3, 0.3],
              loc='upper center',cellLoc='center')
    plt.table(cellText=stats_df.values,
              rowLabels=stats_df.index,
              colLabels=stats_df.columns,
              # colWidths=[0.3, 0.3],
              loc='center')

    if show_plot:
        plt.show()


def matplot_stats_summary(network_distribution: NetworkDistribution,
                          function_list: list = ['pdf', 'cdf', 'sf'],
                          table: bool = True,
                          show_plot: bool = True):
    """
    Summarize PDF, CDF and SF functions and display summary table all
    in a single plot.


    Parameters
    -------
    network_distribution: Input NetworkDistribution object

    function_list: List of function to calculate (cdf, pdf etc.). By default pdf, cdf and sf functions are calculated

    table: Bool. If true the summary table is shown. By default is true

    show_plot: Bool. If true show the plot. By default, is True

    """
    sns.set_theme()

    name = network_distribution.distribution_name

    fig = plt.figure(num=f'{name} summary plot', figsize=(13, 7))
    # fig.text(0.5, 0.02, 'Length [m]', ha='center')
    fig.suptitle(name)
    # fig.text(0.04, 0.5, 'Density', va='center', rotation='vertical')

    for i, func_name in enumerate(function_list):

        if func_name == 'pdf':
            plt.subplot(2, 2, i+1)
            matplot_stats_pdf(network_distribution, show_plot=False)
        if func_name == 'cdf':
            plt.subplot(2, 2, i + 1)
            matplot_stats_cdf(network_distribution, show_plot=False)
        if func_name == 'sf':
            plt.subplot(2, 2, i + 1)
            matplot_stats_sf(network_distribution, show_plot=False)

    if table:
        plt.subplot(2, 2, i+2)
        plt.axis("off")
        plt.ylim([0, 8])
        plt.xlim([0, 10])
        matplot_stats_table(network_distribution, show_plot=False)

    plt.tight_layout()

    if show_plot:
        plt.show()


def matplot_stats_uniform(network_fit: NetworkFitter):
    """
    Confront the fitted data with the standard uniform 0,1.

    :param network_fit:
    :return:
    """
    sns.set_theme()

    fitted_list = network_fit.get_fitted_distribution_names()

    fig = plt.figure(num=f'Comparison plot', figsize=(13, 7))

    x_values = np.linspace(0, 1, num=1000)
    uniform_cdf = uniform.cdf(x_values)
    plt.title('Comparison between CDFs')

    plt.plot(x_values, uniform_cdf, 'k-', label='U(0, 1)')

    for fit_name in fitted_list:
        fitter = network_fit.get_fitted_distribution(fit_name)
        cdf = fitter.cdf()
        cdf_freq = ecdf(cdf).cdf
        plt.plot(cdf_freq.quantiles, cdf_freq.probabilities, '--', label=fit_name)

    plt.grid(True)
    plt.legend()
    plt.show()



def matplot_ternary(entity,
                    return_plot: bool = False,
                    show_plot: bool = True):

    """
    Plot the ternary diagram for nodes

    Parameters
    ----------

    entity: The fracability Nodes entity

    return_plot: Bool. If true return the plot. By default, false

    show_plot: Bool. If true show the plot. By default, true.


    """

    figure, tax = ternary.figure(scale=100)
    figure.set_size_inches(10, 10)

    if entity.name == 'FractureNetwork':
        nodes = entity.nodes
    elif entity.name == 'Nodes':
        nodes = entity

    PI, PY, PX = nodes.node_count[: 3]
    points = [(PX, PI, PY)]

    tax.scatter(points, marker='o', color='red', label='Classification')

    for n in range(8):
        n += 1
        A1 = np.array([[1, 1, 1], [0, 0, 1], [-n, 4, 0]])
        B = np.array([1, 0, 4 - n])

        X1 = np.linalg.inv(A1).dot(B) * 100
        if n < 4:
            side = [1, 0, 0]
        else:
            side = [0, 1, 0]
        A2 = np.array([[1, 1, 1], side, [-n, 4, 0]])

        X2 = np.linalg.inv(A2).dot(B) * 100

        tax.line(X1, X2, color='black', linewidth=1, alpha=n / 8)

    ax = tax.get_axes()
    ax.text(76.8, 21.3, 8)
    ax.text(74.8, 23.8, 7)
    ax.text(73.5, 27.9, 6)
    ax.text(71, 32.3, 5)
    ax.text(69.1, 38, 4)
    ax.text(65.8, 45, 3)
    ax.text(62.7, 54, 2)
    ax.text(57, 66.5, 1)

    tax.right_corner_label("X", fontsize=15)
    tax.top_corner_label("I", fontsize=15)
    tax.left_corner_label("Y", fontsize=15)

    tax.get_axes().set_aspect(1)  # This is used to avoid deformation when rescaling the plotter window
    # tax.clear_matplotlib_ticks()
    tax.get_axes().axis('off')
    if return_plot:
        return tax
    else:
        if show_plot:
            plt.show()