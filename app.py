import streamlit as st
import pandas as pd

path_matriz = 'MATRIZ LC.xlsx'
st.title('Matriz Disponibilidad LC')
st.emoji("🦉")

# Diccionario de coordinaciones por áreas
coordinaciones_areas = {
    'PM': ['Incomme', 'Education', 'Performance','VP'],
    'IGV': ['SALES', 'IR/PXP','VP'],
    'IGTa': ['SALES', 'B2B', 'IR/PXP','VP'],
    'FNZ & LM': ['Gobernabilidad', 'Sostenibilidad','VP'],
    'B2C': ['X', 'Y', 'Z','VP'],
    'OGTa': ['Consideration', 'IR', 'PXP','VP'],
    'OGV': ['Consideration', 'IR/PXP','VP'],'LCP':['LCP']
}

areas_corner = {'ICX':['IGTa','IGV'],'OGX':['OGV','OGTa','B2C'],'PwC':['FNZ & LM','PM','LCP']}
todas_coord = set([coordinaciones_areas[key][i] for key in coordinaciones_areas.keys() for i in range(len(coordinaciones_areas[key]))])
todas_areas = set(coordinaciones_areas.keys())
# Carga de datos
data_df = pd.read_excel(path_matriz, sheet_name='DATA')

# Define los filtros (áreas, coordinaciones, roles, características binarias)
areas = data_df['AREA'].unique()
corner = data_df['CORNER'].unique()
roles = data_df['ROL'].unique()
nuevo = data_df['NUEVO'].unique()
pleno = data_df['PLENO'].unique()



# Sidebar para selección de filtros
st.sidebar.title('Filtros')
selected_corner = st.sidebar.multiselect('Corner', corner, corner)

if selected_corner:
    if selected_corner == list(corner):
        selected_area = st.sidebar.multiselect('Área', todas_areas, todas_areas)
        print('Todos los coorners')
    else:
        areas_ = [areas_corner[key][i] for key in areas_corner.keys() for i in range(len(areas_corner[key])) if key in selected_corner]
        selected_area = st.sidebar.multiselect('Área',areas_ ,areas_)

    if selected_area:
        # Actualizar las opciones de coordinación basadas en las áreas seleccionadas
        if selected_area == list(todas_areas):
            selected_coordinacion = st.sidebar.multiselect('Coordinación', todas_coord,todas_coord)
        else:
            coordinaciones = set([coordinaciones_areas[key][i] for key in coordinaciones_areas.keys() for i in range(len(coordinaciones_areas[key])) if key in selected_area])
            selected_coordinacion = st.sidebar.multiselect('Coordinación', coordinaciones, coordinaciones)


        selected_rol = st.sidebar.multiselect('Rol', roles,roles)
        selected_nuevo = st.sidebar.multiselect('Nuevos', nuevo,nuevo)
        selected_pleno = st.sidebar.multiselect('Plenos', pleno,pleno)

        # Selector de día
        days = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO']
        selected_days = st.sidebar.multiselect('Selecciona el día', days,days)
        

        # Filtrar datos según los filtros seleccionados en la hoja "DATA"
        filtered_data = data_df[
            (data_df['AREA'].isin(selected_area)) &
            (data_df['COORDINACION'].isin(selected_coordinacion)) &
            (data_df['ROL'].isin(selected_rol)) &
            (data_df['NUEVO'].isin(selected_nuevo)) &
            (data_df['PLENO'].isin(selected_pleno))
        ]

        
        st.write('---')

        with st.expander("Ver Info de miembros seleccionados"):
            # Muestra de disponibilidad horaria para los miembros filtrados
            st.dataframe(filtered_data)

        horas = ['6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12M',
                        '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM',
                        '8PM', '9PM']
            # Calcular la matriz de disponibilidad para los días seleccionados
        # Calcula la matriz de disponibilidad para los días seleccionados
        def calcular_matriz_disponibilidad(selected_data_df, selected_days, path_matriz):
            matriz_disponibilidad = []

            # Filtra los datos por los días seleccionados
            for day in selected_days:
                day_df = pd.read_excel(path_matriz, sheet_name=day)

                # Filtra la disponibilidad solo para los miembros seleccionados en "DATA"
                filtered_day_df = day_df[day_df['NOMBRE'].isin(selected_data_df['NOMBRE'])]

            
                # Calcula la proporción de miembros ocupados para cada hora
                disponibilidad_por_hora = []
                for hour in horas:  # Horas de 6:00 AM a 9:00 PM
                    total_miembros = len(selected_data_df)
                    miembros_ocupados = len(filtered_day_df[filtered_day_df[f"{hour}"] == 1])
                    proporcion_ocupados = miembros_ocupados / total_miembros if total_miembros > 0 else 0
                    disponibilidad_por_hora.append(round(proporcion_ocupados, 2))

                matriz_disponibilidad.append(disponibilidad_por_hora)

            return matriz_disponibilidad

        # Después del bucle de días seleccionados, agregar lo siguiente:
        if selected_days:
            # Calcular la matriz de disponibilidad
            matriz_disponibilidad = calcular_matriz_disponibilidad(filtered_data, selected_days, path_matriz)

            # Crear un DataFrame para mostrar la matriz
            matriz_df = pd.DataFrame(matriz_disponibilidad, columns=horas, index=selected_days)

            # Mostrar la matriz de disponibilidad
            st.write('Matriz de Disponibilidad')
            st.write(matriz_df)
            days_tabs = st.tabs(selected_days)


            # Carga de la hoja de disponibilidad del día seleccionado
            for i,tab in enumerate(days_tabs):
                with tab:
                    day_df = pd.read_excel(path_matriz, sheet_name=selected_days[i])

                    # Filtra la disponibilidad solo para los miembros seleccionados en "DATA"
                    filtered_day_df = day_df[day_df['NOMBRE'].isin(filtered_data['NOMBRE'])]

                    # Muestra de disponibilidad horaria para el día seleccionado
                    st.write(f'Disponibilidad para el día {selected_days[i]}')
                    st.dataframe(filtered_day_df)
    else:
        st.write(f'Debes Seleccionar Filtros')
    
else:
    st.write(f'Debes Seleccionar Filtros')