# -*- coding: utf-8 -*-
"""CloudGenix-demo-flowsankey.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pVfxnuCWZsV71sG3WNK5NNKIDdlenBxV
"""

# these lines should be in google collab notebook.
# Install cloudgenix SDK in Runtime (may need restart - will prompt). Can add add'l lines for any other non-default
# modules you need (pandas, etc)
# !pip install --upgrade cloudgenix
# !pip install --upgrade cloudgenix_idname
# !pip install --upgrade fuzzywuzzy
# !pip install --upgrade python-Levenshtein
# !pip install plotly==4.5.2


# these functions should be in notebook.
# Import and Instantiate the API
import cloudgenix
import cloudgenix_idname
import pandas as pd
import plotly.graph_objects as go
import IPython
import ipywidgets
from IPython.display import display, Javascript
from cloudgenix import jd, jd_detailed
from fuzzywuzzy import process

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
try:
    pd.set_option('display.max_colwidth', None)
except ValueError:
    # seriously pandas???? :P
    pd.set_option('display.max_colwidth', -1)


def instantiate():
    # import cloudGenix SDK
    sdk = cloudgenix.API()
    return sdk


def ask_for_auth_token_and_login(sdk):
    # Prompt the user for the secret AUTH_TOKEN as a hidden string paste interactively
    import getpass
    AUTH_TOKEN = getpass.getpass("controller - Paste your AUTH_TOKEN Here:")

    # make a safely loggable string from CGX AUTH_TOKEN so you can verify token is not corrupted.
    session_id_char = str(AUTH_TOKEN).find("session_key=")
    if session_id_char < 0:
        # invalid auth_token.
        auth_token_loggable = "<CORRUPTED AUTH TOKEN: {0}>".format(AUTH_TOKEN)
    else:
        session_start_char = session_id_char + len("session_key=")
        auth_token_loggable = AUTH_TOKEN[session_start_char:session_start_char + 127]

    print(f"Got AUTH_TOKEN with Session ID: {auth_token_loggable}")

    # Login to the API. If AUTH_TOKEN set use that, otherwise prompt.
    if AUTH_TOKEN:
        login_status = sdk.interactive.use_token(AUTH_TOKEN)
    else:
        login_status = sdk.interactive.login()

    print("Login Status: {0}".format("Success" if login_status else "Failure"))


def create_api_maps_cache(sdk):
    # Get ID-> Name maps.
    # create constructor
    idname = cloudgenix_idname.CloudGenixIDName(sdk)

    print("Generating maps, this may take a bit..")
    all_id2n = idname.generate_sites_map()
    all_id2n.update(idname.generate_sites_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_elements_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_machines_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_policysets_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_securitypolicysets_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_securityzones_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_networkpolicysetstacks_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_networkpolicysets_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_prioritypolicysetstacks_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_prioritypolicysets_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_waninterfacelabels_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_wannetworks_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_wanoverlays_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_servicebindingmaps_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_serviceendpoints_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_ipsecprofiles_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_networkcontexts_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_appdefs_map(key_val='id', value_val='display_name'))
    all_id2n.update(idname.generate_natglobalprefixes_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_natlocalprefixes_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_natpolicypools_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_natpolicysetstacks_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_natpolicysets_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_natzones_map(key_val='id', value_val='name'))
    # all_id2n.update(idname.generate_tenant_operators_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_topology_map(key_val='path_id', value_val='idnamev2'))
    all_id2n.update(idname.generate_anynets_map(key_val='path_id', value_val='name'))
    all_id2n.update(idname.generate_interfaces_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_waninterfaces_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_lannetworks_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_spokeclusters_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_localprefixfilters_map(key_val='id', value_val='name'))
    all_id2n.update(idname.generate_globalprefixfilters_map(key_val='id', value_val='name'))

    if all_id2n:
        print(f"Got {len(all_id2n)} ID-> Name entries.")

    # Generate Site, Element, and App Name to ID maps.
    sites_n2id = idname.generate_sites_map(key_val="name", value_val="id")
    if sites_n2id:
        print(f"Got {len(sites_n2id)} Site entries.")

    elements_n2id = idname.generate_elements_map(key_val="name", value_val="id")
    if elements_n2id:
        print(f"Got {len(elements_n2id)} Element entries.")

    apps_n2id = idname.generate_appdefs_map(key_val="display_name", value_val="id")
    if apps_n2id:
        print(f"Got {len(apps_n2id)} App entries.")

    return idname, all_id2n, sites_n2id, elements_n2id, apps_n2id


# # Get Site from form Based on name. This should be in notebook.
# #@title Enter Site Name
# site_name = "Branch1" #@param {type:"string"}


def select_site(site_name, sites_n2id):
    sites_list = sites_n2id.keys()
    possibilities = process.extract(site_name, sites_list, limit=7)
    site_choice, site_percent = possibilities[0]
    # perfect match, just get..
    if site_percent == 100:
        site_id = sites_n2id[site_choice]

    # good guess match..
    elif site_percent > 50:

        print(f"I think you meant *{site_choice}*, using that..")
        site_id = sites_n2id[site_choice]

    # Not got good confidence.
    else:
        print(f"No match for {site_name}, please reenter. Here's what near to entry:")
        for choice, percent in possibilities:
            print(f"   {choice}, ({percent}%)")
        site_id = None

    print(f"Site ID Selected: {site_id}")

    return site_id


# # Get element from form Based on name. This should be in notebook.
# #@title Enter Element Name
# element_name = "BR1-1" #@param {type:"string"}


def select_element(element_name, elements_n2id):
    elements_list = elements_n2id.keys()
    possibilities = process.extract(element_name, elements_list, limit=7)
    element_choice, element_percent = possibilities[0]
    # perfect match, just get..
    if element_percent == 100:
        element_id = elements_n2id[element_choice]

    # good guess match..
    elif element_percent > 50:

        print(f"I think you meant *{element_choice}*, using that..")
        element_id = elements_n2id[element_choice]

    # Not got good confidence.
    else:
        print(f"No match for {element_name}, please reenter. Here's what near to entry:")
        for choice, percent in possibilities:
            print(f"   {choice}, ({percent}%)")
        element_id = None

    print(f"Element ID Selected: {element_id}")


# Declare selected app list
selected_app_list = []

# # Get app from form Based on name. Should be in notebook.
# # @title Enter App Name
# app_name = "salesforce"  # @param {type:"string"}


def select_app(app_name, app_list, apps_n2id):
    if not isinstance(app_list, list):
        print(f"First argument must be a List of App IDs. Got {type(app_list)}.")
        return

    apps_all_list = apps_n2id.keys()

    possibilities = process.extract(app_name, apps_all_list, limit=7)
    app_choice, app_percent = possibilities[0]
    # perfect match, just get..
    if app_percent == 100:
        app_id = apps_n2id[app_choice]

    # good guess match..
    elif app_percent > 50:

        print(f"I think you meant *{app_choice}*, using that..")
        app_id = apps_n2id[app_choice]

    # Not got good confidence.
    else:
        print(f"No match for {app_name}, please reenter. Here's what near to entry:")
        for choice, percent in possibilities:
            print(f"   {choice}, ({percent}%)")
        app_id = None

    if app_id is not None:
        app_list.append(app_id)
        print(f"App ID {app_id} added to list. Total Entries: {len(app_list)}")
        return
    else:
        # just return
        return


#
# button = ipywidgets.Button(description="Add App to selected list.",
#                            layout=ipywidgets.Layout(width='20%', height='30px'))
# output = ipywidgets.Output()

# def on_button_clicked(b):
#   # Display the message within the output widget.
#   global selected_app_list
#   with output:
#     selected_app_list.append(app_id)
#     print(f"Added *{app_choice}* to selected app list ({len(selected_app_list)} items selected.)")


# load flows and put into a dataframe

def query_flows_to_df(sdk, all_id2n, start_time, end_time, site_id, app_id_list=None, destination_ips=None,
                      destination_ports=None, protocol=None, source_ips=None, source_ports=None):
    flow_query = {
        "start_time": start_time,  # "2020-02-26T19:52:45.721Z",
        "end_time": end_time,  # "2020-02-26T20:52:45.721Z",
        "filter": {
            "site": [
                site_id
            ],
        },
        "debug_level": "all"
    }
    if app_id_list and isinstance(app_id_list, list):
        flow_query["filter"]["app"] = app_id_list
    elif app_id_list:
        # not list, just add as single value in list.
        flow_query["filter"]["app"] = [app_id_list]

    flow = {}
    if destination_ips:
        if isinstance(destination_ips, list):
            flow["destination_ip"] = destination_ips
        else:
            # single item - make list
            flow["destination_ip"] = [destination_ips]

    if destination_ports:
        if isinstance(destination_ports, list):
            flow["destination_port"] = destination_ports
        else:
            # single item - make list
            flow["destination_port"] = [destination_ports]

    if source_ips:
        if isinstance(source_ips, list):
            flow["source_ip"] = source_ips
        else:
            # single item - make list
            flow["source_ip"] = [source_ips]

    if source_ports:
        if isinstance(source_ports, list):
            flow["source_port"] = source_ports
        else:
            # single item - make list
            flow["source_port"] = [source_ports]

    if protocol:
        flow["protocol"] = protocol

    # check and see if we got anything
    if flow:
        flow_query["filter"]["flow"] = flow

    resp = sdk.post.flows_monitor(flow_query)

    flows = resp.cgx_content.get('flows', {})
    flow_items = flows.get('items')

    if flow_items:
        df = pd.DataFrame(flow_items)

    else:
        df = pd.Dataframe()

    # do id-> name lookups
    for column in df.columns:
        df[column] = df[column].apply(lambda x: all_id2n.get(x, x) if isinstance(x, str) else x)

    # add row_count
    df['row_count'] = 1
    return df


# display(df)

# # Debuging items (Optional)
# sdk.set_debug(3)
# # flush AUTH_TOKEN if this is run
# AUTH_TOKEN=None
# # Make a request to a check IP site to find out this runtimes IP.
# session = sdk.expose_session()
# session.get('http://checkip.dyndns.org').content

# layout = go.Layout(
#     title='Sankey Layout',
#     font=dict(family='Arial', size=18, color='#7f7f7f')
# )


# fig = go.Figure(data=[go.Sankey(
#     node = dict(
#       pad = 15,
#       thickness = 20,
#       line = dict(color = "black", width = 0.5),
#       label = ["A1", "A2", "B1", "B2", "C1", "C2"],
#       color = "blue"
#     ),
#     link = dict(
#       source = [0, 1, 0, 2, 3, 3], # indices correspond to labels, eg A1, A2, A2, B1, ...
#       target = [2, 3, 3, 4, 4, 5],
#       value = [8, 4, 2, 8, 4, 2]
#   ))], layout=layout)


def generate_flow_app_sankey(df, cat_cols=None, value_cols='', title='Sankey Diagram', layout=None,
                             thickness=20, pad=10, line=None):
    if cat_cols is None:
        cat_cols = []
    if layout is None:
        layout = go.Layout(
            title=title,
            height=1750,
            width=1500,
            font=dict(
                family='Arial',
                size=18,
                color='#7f7f7f'
            ))
    if line is None:
        line = dict(
                color="black",
                width=0.5
            )

    # maximum of 6 value cols -> 6 colors
    color_palette = ['#797A7D', '#F37021', '#7ABBE3', '#FFC700', '#646464']
    label_list = []
    color_num_list = []

    if value_cols == '':
        # count rows for pseudo_count
        df['psuedo_count'] = 1
        value_cols = 'psudeo_count'

    for cat_col in cat_cols:
        label_list_temp = list(set(df[cat_col].values))
        color_num_list.append(len(label_list_temp))
        label_list = label_list + label_list_temp

    # remove duplicates from labelList
    label_list = list(dict.fromkeys(label_list))

    # define colors based on number of levels
    color_list = []
    for idx, color_num in enumerate(color_num_list):
        color_list = color_list + [color_palette[idx]] * color_num

    source_target_df = None
    # transform df into a source-target pair
    for i in range(len(cat_cols) - 1):
        if i == 0:
            source_target_df = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            source_target_df.columns = ['source', 'target', 'count']
        else:
            temp_df = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            temp_df.columns = ['source', 'target', 'count']
            source_target_df = pd.concat([source_target_df, temp_df])
        source_target_df = source_target_df.groupby(['source', 'target']).agg({'count': 'sum'}).reset_index()

    # add index for source-target pair
    source_target_df['sourceID'] = source_target_df['source'].apply(lambda x: label_list.index(x))
    source_target_df['targetID'] = source_target_df['target'].apply(lambda x: label_list.index(x))

    # creating the sankey diagram
    data = dict(
        type='sankey',
        arrangement="perpendicular",
        orientation="h",
        node=dict(
            pad=pad,
            thickness=thickness,
            line=line,
            label=label_list,
            color=color_list
        ),
        link=dict(
            source=source_target_df['sourceID'],
            target=source_target_df['targetID'],
            value=source_target_df['count']
        )
    )

    sankey_dict = dict(data=[data], layout=layout)
    # display(sourceTargetDf)

    return go.Figure(**sankey_dict)


# fig = generate_flow_app_sankey(df, ['source_ip', 'app_id', 'destination_ip'], 'row_count')

# jd(sankey_dict['layout'])

# update the output height
# display(Javascript(data='''google.colab.output.setIframeHeight(0, true, {maxHeight: 1700})'''))

# fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
# fig.show()
