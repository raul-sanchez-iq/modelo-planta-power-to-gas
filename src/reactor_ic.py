"""
Módulo del reactor anaerobio de circulación interna (IC).

Primer módulo del modelo de la planta de depuración de aguas residuales de
matadero porcino con integración Power-to-Gas (TFG).
"""

from numbers import Real


def reactor_anaerobio_ic(Q=5561.53, S0=5.6, COV=10, H=20, eta=0.82,
                         rend_CH4=0.35, y_CH4=0.70, Y=0.05, C_fango=30):
    """
    Dimensiona un reactor anaerobio IC y calcula su producción de biogás y fango.

    Parámetros
    ----------
    Q : float
        Caudal de alimentación [m3/d].
    S0 : float
        DQO de entrada [kg DQO/m3].
    COV : float
        Carga orgánica volumétrica de diseño [kg DQO/(m3·d)].
    H : float
        Altura útil del reactor [m].
    eta : float
        Eficiencia de eliminación de DQO, en fracción (0 < eta <= 1) [-].
    rend_CH4 : float
        Rendimiento DQO -> CH4 [Nm3 CH4/kg DQO].
    y_CH4 : float
        Riqueza de metano en el biogás, en fracción (0 < y_CH4 <= 1) [-].
    Y : float
        Coeficiente de crecimiento celular [kg SSV/kg DQO].
    C_fango : float
        Concentración de la purga de fango [kg/m3].

    Devuelve
    --------
    dict o None
        Diccionario con los resultados redondeados a 2 decimales:
        m_DQO_kg_d, V_util_m3, TRH_d, A_teor_m2, v_a_m_h, dm_DQO_kg_d,
        Q_CH4_Nm3_d, Q_biogas_Nm3_d, P_x_kg_d, V_f_m3_d.
        Devuelve None si algún parámetro no es válido.
    """
    parametros = (Q, S0, COV, H, eta, rend_CH4, y_CH4, Y, C_fango)

    # Validación: todos numéricos (se excluye bool) y estrictamente positivos
    for p in parametros:
        if isinstance(p, bool) or not isinstance(p, Real) or not p > 0:
            return None

    # Las fracciones no pueden superar la unidad
    if eta > 1 or y_CH4 > 1:
        return None

    # 1. Carga másica de DQO de entrada [kg DQO/d]
    m_DQO = Q * S0
    # 2. Volumen útil del reactor [m3]
    V_util = m_DQO / COV
    # 3. Tiempo de retención hidráulico [d]
    TRH = V_util / Q
    # 4. Sección teórica del reactor [m2]
    A_teor = V_util / H
    # 5. Velocidad ascensional [m/h] (Q pasado de m3/d a m3/h)
    v_a = (Q / 24) / A_teor
    # 6. DQO eliminada [kg DQO/d]
    dm_DQO = m_DQO * eta
    # 7. Producción de metano [Nm3 CH4/d]
    Q_CH4 = dm_DQO * rend_CH4
    # 8. Producción de biogás [Nm3/d]
    Q_biogas = Q_CH4 / y_CH4
    # 9. Producción de fango (biomasa) [kg SSV/d]
    P_x = Y * dm_DQO
    # 10. Caudal de purga de fango [m3/d]
    V_f = P_x / C_fango

    # Se redondea solo al final para no arrastrar errores de redondeo
    return {
        "m_DQO_kg_d": round(m_DQO, 2),
        "V_util_m3": round(V_util, 2),
        "TRH_d": round(TRH, 2),
        "A_teor_m2": round(A_teor, 2),
        "v_a_m_h": round(v_a, 2),
        "dm_DQO_kg_d": round(dm_DQO, 2),
        "Q_CH4_Nm3_d": round(Q_CH4, 2),
        "Q_biogas_Nm3_d": round(Q_biogas, 2),
        "P_x_kg_d": round(P_x, 2),
        "V_f_m3_d": round(V_f, 2),
    }


if __name__ == "__main__":
    # Caso de prueba con los valores por defecto
    esperado = {
        "m_DQO_kg_d": 31144.57, "V_util_m3": 3114.46, "TRH_d": 0.56,
        "A_teor_m2": 155.72, "v_a_m_h": 1.49, "dm_DQO_kg_d": 25538.55,
        "Q_CH4_Nm3_d": 8938.49, "Q_biogas_Nm3_d": 12769.27,
        "P_x_kg_d": 1276.93, "V_f_m3_d": 42.56,
    }
    resultado = reactor_anaerobio_ic()
    assert resultado == esperado, resultado

    # Casos inválidos: deben devolver None
    assert reactor_anaerobio_ic(Q=0) is None
    assert reactor_anaerobio_ic(S0=-1) is None
    assert reactor_anaerobio_ic(eta=82) is None      # porcentaje en vez de fracción
    assert reactor_anaerobio_ic(y_CH4=1.2) is None
    assert reactor_anaerobio_ic(H="20") is None

    for clave, valor in resultado.items():
        print(f"{clave:<16} = {valor}")
    print("Todas las pruebas superadas.")
