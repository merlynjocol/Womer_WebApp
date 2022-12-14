import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import CategoricalDtype




# Data upload
# enter to project / details / API / endpoints
url_info= "https://five.epicollect.net/api/export/entries/mujeres-y-recursos?form_ref=de37bfdc5fc246c2b7e5a68dec3ca944_6306549b3c43c&format=csv&per_page=1000&page=1"
data = pd.read_csv(url_info)


#change the columns names
dict = {'3_Cul_es_la_comunida' : "community",
            '4_Qu_tipo_de_cocina_' : "kitchen", 
            '5_Su_estufa_tiene_ch' : 'chimenea', 
            '6_Qu_energa_o_combus' : 'energy_cook', 
            '7_Quin_est_a_cargo_d' : 'Who_cook',
            '8_Cunto_tiempo_toma_' : 'time_cook',
            '9_Qu_transporte_se_u' : 'transport_energy', 
            '10_Cunto_tiempo_toma' : 'time_transport_energy', 
            '11_Quin_est_a_cargo_' : 'who_transport_energy',
            '12_Qu_usa_para_calen' : 'how_heating',
            '13_Qu_tipo_de_combus' :  'energy_heating',
            '14_Qu_usa_para_enfri' : 'how_cooling',
            '15_Con_qu_energa_o_c' :  'energy_cooling',
            '16_Que_utiliza_para_' :  'how_lighting',
            '17_En_su_hogar_se_pa'  :'energy_payment',
            '19_Quin_principalmen'  : 'who_pay_energy',
            '20__Cul_es_la_PRINCI'  : 'water_source',
            '21_Dnde_se_encuentra' : 'water_where',
            '22_En_su_hogar_se_ut'  : 'water_access',
            '23_Qu_modo_de_transp'  : 'water_transport',
            '24_Cunto_tiempo_toma' : 'water_time',
            '25_Cul_es_la_persona'  : 'who_transport_water',
            '26_Cuntas_viajes_se_'  : 'frequency_transport_water',
            '27_Su_PRINCIPAL_fuen' : 'water_disponibility',
            '28_En_los_ltimos_12_'  : 'last_12month_water',
            '29_Cuando_no_ha_teni'  : 'reason_no_water',
            '31_Cuenta_su_hogar_c'  : 'water_deposit',
            '32_En_el_ltimo_mes_h'  : 'last_month_water_deposit',
            '33_Cul_es_el_servici' :  'sanitary_service',
            '35_El_servicio_sanit'  : 'sanitary_light_lock',
            '36_Dnde_se_encuentra' : 'sanitary_where',
            '37_Comparte_el_servi'  : 'sanitary_sharing',
            '38_Otras_personas_pu'  : 'sanitary_security',
            '39_Hay_algn_riesgo_p' :  'sanitary_risk',
            '41_La_instalacin_tie'  : 'sanitary_hands',
            '42_Utiliza_alguno_de' : 'hand_wash',
            '44_Durante_su_ltimo_'  : 'female_privacity',
            '45_Cul_es_el_materia' : 'female_hygiene',
            '47_No_pudo_participa'  : 'female_participation',
            '49_Quin_es_la_person'  : 'who_wild_food',
            '50_Cunto_tiempo_esta'  : 'time_wild_food', 
            '51_Quin_es_la_person' : 'who_fishing',
            '52_Cunto_tiempo_esta'  : 'time_fishing',
            '53_Quin_es_la_person' : 'who_crops',
            '54_Cunto_tiempo_esta' : 'time_crops'
}

# call rename () method
data.rename(columns=dict,
          inplace=True)

df = data.copy(deep=True)



def app():
    """
    Main app that streamlit will render.
    """
    st.title("??? Indicadores de acceso a Recursos Naturales ")
    st.markdown ('---')

    
    # MULTIPAGES SELECTOR 
    # create your radio button with the index that we loaded

    st.sidebar.markdown ('---')
    st.subheader("Selecciona un ??rea de an??lisis")
    choice = st.radio(" ", ('Energ??a (Iluminaci??n y Cocina)','Agua','Saneamiento', 'Alimentos' ))
    st.markdown ('---')


    # df in percentage
    def percentage(column):
        df = (column.value_counts()/column.count())*100
        df = (df.to_frame().reset_index())
        df = df.round(decimals = 1)
        return df

    # Titles charts
    def format_title(title, subtitle=None, subtitle_font_size=16):
        title = f'<b>{title}</b>'
        if not subtitle:
            return title
        subtitle = f'<span style="font-size: {subtitle_font_size}px;">{subtitle}</span>'
        return f'{title}<br>{subtitle}'   


    if choice == 'Energ??a (Iluminaci??n y Cocina)':

      
        #Energy
        st.subheader("## ?????? Indicadores de Acceso a Energ??a")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Proporci??n de la poblaci??n que tiene acceso a la electricidad para iluminaci??n",
         'Proporci??n de la poblaci??n cuya fuente primaria de energ??a son los combustibles y tecnolog??as limpios',
         'Tiempo dedicado a recolectar combustible para el consumo dom??stico',
         'Tipo de estufa utilizada para cocinar',
         "Proporci??n de hogares que utilizan estufas con chimenea",
         "Tiempo dedicado a cocinar los alimentos",    
            
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ?????? Por favor seleccione un indicador")
            st.stop()

        # Interactive visualization 
        if indicator == "Proporci??n de la poblaci??n que tiene acceso a la electricidad para iluminaci??n": 
            
            #title
            #st.write("#### Proporci??n de la poblaci??n que tiene acceso a la electricidad")
            st.write( '#### ODS7. Indicador 7.1.1.')
            st.write("En el marco de la meta .mundial de igualdad de acceso a la energ??a, el ODS 7.1.1 se centra espec??ficamente en el acceso a la electricidad disponible para la poblaci??n mundial. Para obtener una imagen clara, las tarifas de acceso solo se consideran si el fuente principal de iluminaci??n es el proveedor local de electricidad, sistemas solares, mini-redes y aut??nomos sistemas Fuentes como generadores, velas, bater??as, etc., no se consideran por su limitada capacidades de trabajo y dado que generalmente se mantienen como fuentes de respaldo para la iluminaci??n")

            def conditions(s):
                if (s == 'Lamparas solares' ) or (s == '"L??mpara de gasolina, queroseno"' ) or (s == '"L??mpara de gasolina, queroseno", Vela' )or (s == 'Linterna de pilas recargable, Vela') or  (s == 'L??mpara de aceite o parafina, Vela, Linterna de pilas recargable'): 
                    return "No"
                
                else:
                    return "Si"

            df['Electricity'] = df['how_lighting'].apply(conditions)

            electricity =  percentage(df.Electricity)

            fig_pie = px.pie(electricity, values='Electricity', names='index', color='index',
                                    color_discrete_map={'No':'lightslategray',  'Si':'#f9ab0c'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres con acceso a la Electricidad",
                                                "Iluminaci??n"),
                            title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua ind??gena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)



        elif indicator == 'Proporci??n de la poblaci??n cuya fuente primaria de energ??a son los combustibles y tecnolog??as limpios':  
            
           #title
            st.write("### ODS7. Indicador 7.1.2. ")
            st. write("Proporci??n de la poblaci??n cuya fuente primaria de energ??a son los combustibles y tecnolog??as limpias")
            
            def conditions(s):
                if (s == 'Lamparas solares' ): 
                    return "Energ??as limpias"
                else:
                    return "Energias f??siles o qu??micas"
            
            df['clean_fuel'] = df['how_lighting'].apply(conditions)
            clean_fuel =  percentage(df.clean_fuel)

            fig_pie = px.pie(clean_fuel, values='clean_fuel', names='index', color='index',
                                    color_discrete_map={'Energ??as limpias':'#f9ab0c',  'Energias f??siles o qu??micas':'lightslategray'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres con acceso a Energ??as limpias",
                                                        "Iluminaci??n"),
                                        title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua ind??gena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)


        # Kithchen type
        elif indicator == 'Tipo de estufa utilizada para cocinar':
            #st. write('Tipo de estufa utilizada para cocinar')
            kitchen =  percentage(df.kitchen)

            # stablishing catgeories WASH
            categories = CategoricalDtype(['Estufa el??ctrica',
                                        'Estufa de biog??s ',
                                        'Estufa de gas propano con pipa de gas',
                                        'Estufa de combustible: Gasolina, ACPM, Kerosene', 
                                        'Estufa de le??a',
                                        'Fuego abierto'])

            kitchen["index"] = kitchen["index"].astype(categories)
            kitchen = kitchen.sort_values('index')
            #chart
            colors = ['lightslategray']*len(df)
            colors[ 3 ] = '#f9ab0c'
            colors[ 4 ] = '#f9ab0c'
            colors[ 5 ] = '#f9ab0c'
            fig = px.bar(kitchen, x="kitchen", y="index",  
                                width=600, height=300, 
                                labels={ 'kitchen': 'Proporci??n (%)',  'index': 'Tipo de Cocinas)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("% Tipo de Cocinas utilizadas por las Mujeres",
                                                "con m??s riesgo de afectaci??n por contaminaci??n ambiental "),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)


        elif indicator ==  "Proporci??n de hogares que utilizan estufas con chimenea":
            st. write("Este indicador muestra la proporci??n de mujeres a exposici??n por contaminaci??n de humo")
            chimenea =  percentage(df.chimenea)

            fig_pie = px.pie(chimenea, values='chimenea', names='index', color='index',
                                    color_discrete_map={'No':'crimson',  'Si':'lightslategray'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres usando chimenea en la cocina",
                                                "Para eliminaci??n de aire contaminado"),
                            title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua ind??gena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)


        elif indicator ==   "Tiempo dedicado a cocinar los alimentos":

            #title
            #st. write("### Tiempo dedicado a cocinar los alimentos")
            # tiempo en cocinar alimentos 
            time_cook =  percentage(df.time_cook)
            time_cook = time_cook.sort_values('index')
            colors = ['lightslategray']*len(df)
            colors[ 2 ] = '#f9ab0c'
            fig = px.bar(time_cook, x="time_cook", y="index",  
                                width=600, height=300, 
                                labels={ 'time_cook': 'Proporci??n de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo invertido en Cocinar alimentos",
                                                "% Mujeres "),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)


        elif indicator == 'Tiempo dedicado a recolectar combustible para el consumo dom??stico':

            #title
            #st. write("### Tiempo dedicado a recolectar combustible para el consumo dom??stico")
            #st.write( 'SDG. Indicador 7.1.2. ')
            
            time_transport_energy =  percentage(df.time_transport_energy)

            time_transport_energy['index'].unique()

            # stablishing catgeories WASH
            categories = CategoricalDtype(['Menos de 1 hora',
                                        '1 hora ',
                                        '2 horas',
                                        '3 horas',
                                        '4 horas ',
                                        'No se '])



            time_transport_energy['index'] =time_transport_energy['index'].astype(categories)
            time_transport_energy = time_transport_energy.sort_values('index')

            colors = ['lightslategray']*len(df)
            colors[ 2 ] = '#f9ab0c'


            #opacity = 0.8

            fig = px.bar(time_transport_energy, x="time_transport_energy", y="index",  
                                width=600, height=300, 
                                labels={ 'time_cook': 'Proporci??n de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo invertido en transportar combustible",
                                                "Para uso dom??stico: cocina. % Mujeres "),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

    elif choice == 'Agua': 

        #AGUA
        st.subheader("## ???? Indicadores de acceso a agua para consumo")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Proporci??n de la poblaci??n que utiliza servicios de suministro de agua potable gestionados sin riesgos. Por Instalaci??n",
         "Proporci??n de la poblaci??n que utiliza servicios de agua para consumo gestionados de manera insegura",
         'Tiempo dedicado a transportar agua para consumo dom??stico',
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ?????? Por favor seleccione un indicador")
            st.stop()

        # Interactive visualization 
        if indicator == "Proporci??n de la poblaci??n que utiliza servicios de suministro de agua potable gestionados sin riesgos. Por Instalaci??n": 

            #title
            st. write("### Proporci??n de la poblaci??n que utiliza servicios de suministro de agua potable gestionados sin riesgos")
            st.write( 'SDG. Indicador 6.1.1. ')

            water_source =  percentage(df.water_source)

            # stablishing catgeories WASH
            categories = CategoricalDtype(['Agua de una quebrada, nacimiento ?? manantial NO protegida',
                                        'Agua de una quebrada, nacimiento ?? manantial protegida',
                                        'Pozo sin bomba, aljibe, jag??ey o barreno ',
                                        'Pozo con bomba ',
                                        'Llave o grifo p??blico ',
                                        'Otra fuente por tuber??a ', 
                                        'Acueducto con tuber??a dentro de la vivienda '])



            water_source['index'] = water_source['index'].astype(categories)
            water_source = water_source.sort_values('index')

            colors = ['#DCDCDC',]*len(df)
            colors[ 6 ] = '#4086ce'
            #opacity = 0.8

            fig = px.bar(water_source, x="water_source", y="index",  
                                width=700, height=300, 
                                labels={ 'water_source': 'Proporci??n (%)',  'index': 'Fuente de Agua)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Agua para Consumo",
                                                "Gestionados de Manera Segura. Por Instalaci??n"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator == "Proporci??n de la poblaci??n que utiliza servicios de agua para consumo gestionados de manera insegura":

            def conditions(s):
                if (s == 'Agua de una quebrada, nacimiento ?? manantial NO protegida' ) or (s == 'Agua de una quebrada, nacimiento ?? manantial protegida' ) or (s == 'Pozo sin bomba, aljibe, jag??ey o barreno ' ): 
                    return "Agua superficial"
                
                if (s == 'Pozo con bomba ' ): 
                    return "Instalaci??n no mejorada"
                if (s == 'Llave o grifo p??blico ' ): 
                    return "Servicio limitado"
                if (s == 'Otra fuente por tuber??a ' ): 
                    return "Servicio b??sico"
                else:
                    return "Servicio gestionado de manera segura"


            water_source =  percentage(df.water_source)
            water_source['WASH'] = water_source['index'].apply(conditions)

            fig = px.bar(water_source,x="water_source", y="WASH", color="WASH", 
                        labels={ 'water_source': 'Proporci??n (%)',  'WASH': 'Servicio'},
                        width=700, height=300, 
                        color_discrete_map={'Agua superficial': '#f9ab0c',
                                                'Instalaci??n no mejorada': '#fcd434',
                                                'Servicio limitado': '#faf559',
                                                'Servicio b??sico': '#DCDCDC', 
                                                'Servicio gestionado de manera segura': '#DCDCDC'},
                        template = "simple_white"
                        )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Agua para Consumo",
                                                "Por categorias del Servicio"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_yaxes(visible=True, showticklabels=False)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)



        elif indicator == 'Tiempo dedicado a transportar agua para consumo dom??stico':

            # tiempo en cocinar alimentos 
            water_time =  percentage(df.water_time)



            colors = ['lightslategray']*len(df)
            colors[ 0 ] = '#f9ab0c'
            colors[ 1 ] = '#f9ab0c'


            #opacity = 0.8

            fig = px.bar(water_time, x="water_time", y="index",  
                                width=600, height=300, 
                                labels={ 'water_time': 'Proporci??n de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo invertido en Transportar Agua",
                                                "Para cocinar alimentos"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

    elif choice == 'Saneamiento': 

        #AGUA
        st.subheader("## ???? Indicadores de acceso a Servicio de Saneamiento")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Proporci??n de Mujeres que utiliza servicios de saneamiento gestionados de forma segura",
         "Proporci??n de Mujeres segun servicio de saneamiento",
         'Proporci??n de Mujeres con servicios de saneamiento con puerta de seguridad e iluminaci??n',
         "Proporci??n de mujeres que enfrentan riesgos al usar los servicios de saneamiento",
         "Proporci??n de la poblaci??n que utiliza instalaciones para lavarse las manos con agua y jab??n",
         "Proporci??n de mujeres con acceso a instalaciones privadas durante el per??odo menstrual"       
        
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ?????? Por favor seleccione un indicador")
            st.stop()


        sanitary_service  =  percentage(df.sanitary_service)
        df2 = pd.DataFrame({'index': ['Inodoro conectado a alcantarillado',
                              'Letrina de doble pozo', 
                              'Letrina colgante construida sobre una superficie de agua'],
                            'sanitary_service': [0,0,0],
                             })

        # Append the rows of the above pandas DataFrame to the existing pandas DataFrame
        sanitary_service = sanitary_service.append(df2,ignore_index=True)

        # stablishing catgeories WASH
        categories = CategoricalDtype(['Inodoro conectado a alcantarillado',
                                        'Inodoro conectado a pozo o tanque s??ptico ',
                                        'Inodoro a drenaje abierto',
                                        'Inodoro con destino desconocido',
                                        'Letrina de pozo',
                                        'Letrina de doble pozo',
                                        'Letrina de fosa con losa',
                                        'Letrina de fosa sin losa  o  pozo abierto',
                                        'Otra letrina de compostaje',
                                        'Letrina colgante construida sobre una superficie de agua',
                                        'Letrina con descarga a una fuente de agua, rio, laguna, etc',
                                        'Cubo, recipiente o contenedor',
                                        'No tengo instalaci??n. Monte, campo abierto, playa, rio, laguna',
                                            ])

        sanitary_service["index"] = sanitary_service["index"].astype(categories)
        sanitary_service= sanitary_service.sort_values('index')
        
        # Interactive visualization 
        if indicator == "Proporci??n de Mujeres que utiliza servicios de saneamiento gestionados de forma segura":

            colors = ['#DCDCDC',]*len(df)
            colors[ 0 ] = '#4086ce'
            colors[ 1 ] = '#4086ce'
            colors[ 2 ] = '#4086ce'
            #opacity = 0.8

            fig = px.bar(sanitary_service, x="sanitary_service", y="index",  
                                width=700, height=500, 
                                labels={ 'sanitary_service': 'Proporci??n (%)',  'index': 'Servicio)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Saneamiento",
                                                "Gestionados de Manera Segura"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)



        elif indicator == "Proporci??n de Mujeres segun servicio de saneamiento":
            def conditions(s):
                if (s == 'Inodoro conectado a alcantarillado' ) or (s == 'Inodoro conectado a pozo o tanque s??ptico ' ) or (s ==  'Inodoro a drenaje abierto' ) : 
                    return "Servicio gestionado de manera segura"
            
                if (s == 'Inodoro con destino desconocido') or (s == 'Letrina de pozo') or (s == 'Letrina de fosa con losa')or (s == 'Letrina de doble pozo') : 
                    return "Servicio B??sico"
                if (s== 'Letrina de fosa sin losa  o  pozo abierto' ) or ( s== 'Otra letrina de compostaje'): 
                    return "Servicio limitado"
                if (s == 'Letrina colgante construida sobre una superficie de agua'): 
                    return "Instalaci??n no mejorada"
                else:
                    return "Defecaci??n al aire libre"

            sanitary_service['Service'] = sanitary_service['index'].apply(conditions)

            fig = px.bar(sanitary_service,x="sanitary_service", y='Service', color='Service', 
                        labels={ 'sanitary_service': 'Proporci??n (%)',  'Service': 'Servicio'},
                        width=700, height=300, 
                        color_discrete_map={'Defecaci??n al aire libre': '#f9ab0c',
                                                'Instalaci??n no mejorada': '#fcd434',
                                                'Servicio limitado': '#faf559',
                                                'Servicio B??sico': '#DCDCDC', 
                                                'Servicio gestionado de manera segura': '#DCDCDC'},
                            )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Saneamiento",
                                                "Gestionados de Manera insegura"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=False)
            #fig.update_yaxes(visible=True, showticklabels=False)
            fig.update_layout(template = "simple_white")
            #fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            fig.update_traces(showlegend=False)
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator== "Proporci??n de Mujeres con servicios de saneamiento con puerta de seguridad e iluminaci??n": 


            # Lighting and Security in Sanitary services 
            sanitary_light_lock=  percentage(df.sanitary_light_lock)

            colors = ['lightslategray']*len(df)
            colors[ 3 ] = 'crimson'

            #opacity = 0.8

            fig = px.bar(sanitary_light_lock, x="sanitary_light_lock", y="index",  
                                width=600, height=300, 
                                labels={ 'sanitary_light_lock': 'Proporci??n (%)',  'index': 'Servicio)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("% Mujeres con iluminaci??n y cerradura",
                                                "En el servicio de saneamiento"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator== "Proporci??n de mujeres que enfrentan riesgos al usar los servicios de saneamiento": 
            
            # risk for women 
            sanitary_risk =  percentage(df.sanitary_risk)

            colors = ['lightslategray']*len(df)
            colors[ 3 ] = 'crimson'
            colors[ 2 ] = 'crimson'
            colors[ 1 ] = 'crimson'


            #opacity = 0.8

            fig = px.bar(sanitary_risk , x="sanitary_risk", y="index",  
                                width=600, height=300, 
                                labels={ 'sanitary_risk ': 'Proporci??n (%)',  'index': 'Servicio'},
                                template = "simple_white", orientation='h',
                                )
            fig.update_layout(title = format_title("% Mujeres enfrentando riesgos",
                                                "Por el uso del Servicio de Saneamiento"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator == "Proporci??n de la poblaci??n que utiliza instalaciones para lavarse las manos con agua y jab??n":
            
            # infraestructure
            sanitary_hands =  percentage(df.sanitary_hands)

            fig_pie = px.pie(sanitary_hands, values='sanitary_hands', names='index', color='index',
                                    color_discrete_map={'No':'crimson',  'Si':'lightslategray'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres utilizando instalaciones",
                                                "para el lavado de manos con agua y jab??n"),
                            title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua ind??gena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)

        elif indicator ==  "Proporci??n de mujeres con acceso a instalaciones privadas durante el per??odo menstrual" : 

            female_privacity =  percentage(df.female_privacity)

            fig_pie = px.pie(female_privacity, values='female_privacity', names='index', color='index',
                                    color_discrete_map={'No he tenido privacidad':'#9F4F86',  'Si tengo privacidad':'lightslategray'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres con privacidad",
                                                "Durante el periodo menstrual"),
                            title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua ind??gena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)



     
    elif choice == 'Alimentos': 

        st.subheader("## ???? Indicadores de acceso a Alimentos")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Tiempo dedicado a recolectar plantas, hongos, flores y frutos silvestres de los bosques",
         "Quien recolecta los alimentos silvestres",
         "Tiempo dedicado a la caza y la pesca para el consumo dom??stico",
         "Quien pesca y caza para el hogar", 
         "??Quien cultiva alimentos con practicas sostenibles?",
         "Tiempo dedicado al trabajo de cuidados no remunerado en pr??cticas sostenibles. Similar al ODS 5.4.1"       
        
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ?????? Por favor seleccione un indicador")
            st.stop()


        if indicator == "Tiempo dedicado a recolectar plantas, hongos, flores y frutos silvestres de los bosques":

            # tiempo en cocinar alimentos 
            time_wild_food =  percentage(df.time_wild_food)
            time_wild_food = time_wild_food .sort_values('index')

            colors = ['lightslategray']*len(df)
            colors[ 1 ] = 'crimson'


            #opacity = 0.8

            fig = px.bar(time_wild_food, x="time_wild_food", y="index",  
                                width=600, height=300, 
                                labels={ 'time_wild_food': 'Proporci??n de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo invertido en Recolectar Alimentos ",
                                                "Del bosque y otros espacios"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator == "Quien recolecta los alimentos silvestres":

            # tiempo en cocinar alimentos 
            who_wild_food=  percentage(df.who_wild_food)
            who_wild_food = who_wild_food.sort_values('index')

            df_wild_food = pd.DataFrame({'index': ["Hombre mayor de 15 a??os ",
                                                "Ni??a menor de 15 a??os",
                                                    "Ni??o menor de 15 a??os",
                                                    "No s??",
                                                    "No se recolecta alimentos para el hogar "], 'who_wild_food': [0,0,0,0,0],
                                                    })

            # Append the rows of the above pandas DataFrame to the existing pandas DataFrame
            who_wild_food = who_wild_food.append(df_wild_food,ignore_index=True)

            # stablishing catgeories 
            categories = CategoricalDtype(["Yo ",
                                            "Mujer mayor de 15 a??os diferente a mi ",
                                            "Hombre mayor de 15 a??os ",
                                            "Ni??a menor de 15 a??os",
                                            "Ni??o menor de 15 a??os",
                                            "No s??",
                                            "No se recolecta alimentos para el hogar "
                                            ])

            who_wild_food["index"] = who_wild_food["index"].astype(categories)
            who_wild_food= who_wild_food.sort_values('index')    

            #chart
            colors = ['lightslategray']*len(df)
            colors[ 1 ] = 'crimson'
            #opacity = 0.8
            fig = px.bar(who_wild_food, x="who_wild_food", y="index",  
                                width=600, height=300, 
                                labels={ 'who_wild_food': 'Proporci??n de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("??Quien recolecta los alimentos?",
                                                "Plantas, flores, hongos y frutos del bosque y otros espacios"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        
        elif indicator == "Tiempo dedicado a la caza y la pesca para el consumo dom??stico":
            

            # tiempo en hunting and fishing
            time_fishing =  percentage(df.time_fishing)
            time_fishing = time_fishing.sort_values('index')

            # stablishing catgeories 
            categories = CategoricalDtype([ 'Menos de 1 hora',
                                        '1 hora ', 
                                        '2 horas', 
                                        '3 horas', 
                                        '4 horas ',
                                        'M??s de 4 horas ', 
                                        'No se '
                                            ])

            time_fishing["index"] = time_fishing["index"].astype(categories)
            time_fishing = time_fishing.sort_values('index')


            # CHART 
            colors = ['lightslategray']*len(df)
            colors[ 1 ] = 'crimson'
            fig = px.bar(time_fishing, x="time_fishing", y="index",  
                                width=600, height=300, 
                                labels={ 'time_fishing': 'Proporci??n de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo dedicado a la caza y la pesca",
                                                "Para el consumo dom??stico"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)


        elif indicator == "Quien pesca y caza para el hogar":
            # Who is hunting and fishing 
            who_fishing=  percentage(df.who_fishing)
            who_fishing = who_fishing.sort_values('index')

            # Append the rows of the above pandas DataFrame to the existing pandas DataFrame
            df_who_fishing = pd.DataFrame({'index': ["Ni??o menor de 15 a??os",
                                                ], 'who_fishing': [0],
                                                    })
            who_fishing= who_fishing.append(df_who_fishing,ignore_index=True)

            # stablishing categories 
            categories = CategoricalDtype(["Yo ",
                                            "Mujer mayor de 15 a??os diferente a mi ",
                                            "Hombre mayor de 15 a??os ",
                                            "Ni??a menor de 15 a??os",
                                            "Ni??o menor de 15 a??os",
                                            "No s??",
                                            "No se pesca o caza "
                                            ])

            who_fishing["index"] = who_fishing["index"].astype(categories)
            who_fishing= who_fishing.sort_values('index')            

            #chart
            colors = ['lightslategray']*len(df)
            colors[ 1 ] = 'crimson'
            fig = px.bar(who_fishing, x="who_fishing", y="index",  
                                width=600, height=300, 
                                labels={ 'who_fishing': 'Total de hogares',  'index': 'Persona'},
                                template = "simple_white", orientation='h'
                                )

            fig.update_layout(title = format_title("??Quien pesca o caza para el hogar?",
                                                "Plantas, flores, hongos y frutos del bosque y otros espacios"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)


        elif indicator == "??Quien cultiva alimentos con practicas sostenibles?":
            # Quien cultivar en la huerta-crops
            who_crops=  percentage(df.who_crops)
            who_crops = who_crops.sort_values('index')

            # Append the rows of the above pandas DataFrame to the existing pandas DataFrame
            df_who_crops = pd.DataFrame({'index': ["Ni??a menor de 15 a??os",
                                                    "Ni??o menor de 15 a??os",
                                                    "No s??",
                                                    "No se tiene huerta "
                                                ], 'who_crops': [0,0,0,0],
                                                    })

            who_crops= who_crops.append(df_who_crops,ignore_index=True)
            # stablishing catgeories 
            categories = CategoricalDtype(["Yo ",
                                            "Mujer mayor de 15 a??os diferente a mi ",
                                            "Hombre mayor de 15 a??os ",
                                            "Ni??a menor de 15 a??os",
                                            "Ni??o menor de 15 a??os",
                                            "No s??",
                                            "No se tiene huerta "
                                            ])
            who_crops["index"] = who_crops["index"].astype(categories)
            who_crops= who_crops.sort_values('index')            

            #chart
            colors = ['lightslategray']*len(df)
            colors[ 1 ] = 'crimson'
            fig = px.bar(who_crops, x="who_crops", y="index",  
                                width=600, height=300, 
                                labels={ 'who_crops': 'Total de hogares',  'index': 'Persona'},
                                template = "simple_white", orientation='h'
                                )

            fig.update_layout(title = format_title("??Quien cultiva alimentos con practicas sostenibles",
                                                "Practicas ancestrales, agroecolog??a, huertas"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator == "Tiempo dedicado al trabajo de cuidados no remunerado en pr??cticas sostenibles. Similar al ODS 5.4.1":       

            # time sustianable practices crops
            time_crops =  percentage(df.time_crops)
            time_crops = time_crops.sort_values('index')

            # stablishing categories 
            categories = CategoricalDtype([ 'Menos de 1 hora',
                                        '1 hora ', 
                                        '2 horas', 
                                        '3 horas', 
                                        '4 horas ',
                                        'M??s de 4 horas ', 
                                        'No se '
                                            ])

            time_crops["index"] = time_crops["index"].astype(categories)
            time_crops = time_crops.sort_values('index')

            #chart
            colors = ['lightslategray']*len(df)
            colors[ 3 ] = 'crimson'
            fig = px.bar(time_crops, x="time_crops", y="index",  
                                width=600, height=300, 
                                labels={ 'time_crops': 'Proporci??n de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo dedicado a la caza y la pesca",
                                                "Para el consumo dom??stico"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)