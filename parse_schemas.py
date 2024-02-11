import branca.colormap as cm

def get_schema():
    return {
        'owid-energy-data': [
            [
                'country', 'year', 'iso_code', 'population', 'gdp', 'biofuel_cons_change_pct', 'biofuel_cons_change_twh',
                'biofuel_cons_per_capita', 'biofuel_consumption', 'biofuel_elec_per_capita', 'biofuel_electricity',
                'biofuel_share_elec', 'biofuel_share_energy', 'carbon_intensity_elec', 'coal_cons_change_pct',
                'coal_cons_change_twh', 'coal_cons_per_capita', 'coal_consumption', 'coal_elec_per_capita',
                'coal_electricity', 'coal_prod_change_pct', 'coal_prod_change_twh', 'coal_prod_per_capita',
                'coal_production', 'coal_share_elec', 'coal_share_energy', 'electricity_demand', 'electricity_generation',
                'electricity_share_energy', 'energy_cons_change_pct', 'energy_cons_change_twh', 'energy_per_capita',
                'energy_per_gdp', 'fossil_cons_change_pct', 'fossil_cons_change_twh', 'fossil_elec_per_capita',
                'fossil_electricity', 'fossil_energy_per_capita', 'fossil_fuel_consumption', 'fossil_share_elec',
                'fossil_share_energy', 'gas_cons_change_pct', 'gas_cons_change_twh', 'gas_consumption',
                'gas_elec_per_capita', 'gas_electricity', 'gas_energy_per_capita', 'gas_prod_change_pct',
                'gas_prod_change_twh', 'gas_prod_per_capita', 'gas_production', 'gas_share_elec', 'gas_share_energy',
                'greenhouse_gas_emissions', 'hydro_cons_change_pct', 'hydro_cons_change_twh', 'hydro_consumption',
                'hydro_elec_per_capita', 'hydro_electricity', 'hydro_energy_per_capita', 'hydro_share_elec',
                'hydro_share_energy', 'low_carbon_cons_change_pct', 'low_carbon_cons_change_twh', 'low_carbon_consumption',
                'low_carbon_elec_per_capita', 'low_carbon_electricity', 'low_carbon_energy_per_capita',
                'low_carbon_share_elec', 'low_carbon_share_energy', 'net_elec_imports', 'net_elec_imports_share_demand',
                'nuclear_cons_change_pct', 'nuclear_cons_change_twh', 'nuclear_consumption', 'nuclear_elec_per_capita',
                'nuclear_electricity', 'nuclear_energy_per_capita', 'nuclear_share_elec', 'nuclear_share_energy',
                'oil_cons_change_pct', 'oil_cons_change_twh', 'oil_consumption', 'oil_elec_per_capita', 'oil_electricity',
                'oil_energy_per_capita', 'oil_prod_change_pct', 'oil_prod_change_twh', 'oil_prod_per_capita',
                'oil_production', 'oil_share_elec', 'oil_share_energy', 'other_renewable_consumption',
                'other_renewable_electricity', 'other_renewable_exc_biofuel_electricity', 'other_renewables_cons_change_pct',
                'other_renewables_cons_change_twh', 'other_renewables_elec_per_capita',
                'other_renewables_elec_per_capita_exc_biofuel', 'other_renewables_energy_per_capita',
                'other_renewables_share_elec', 'other_renewables_share_elec_exc_biofuel', 'other_renewables_share_energy',
                'per_capita_electricity', 'primary_energy_consumption', 'renewables_cons_change_pct',
                'renewables_cons_change_twh', 'renewables_consumption', 'renewables_elec_per_capita', 'renewables_electricity',
                'renewables_energy_per_capita', 'renewables_share_elec', 'renewables_share_energy', 'solar_cons_change_pct',
                'solar_cons_change_twh', 'solar_consumption', 'solar_elec_per_capita', 'solar_electricity',
                'solar_energy_per_capita', 'solar_share_elec', 'solar_share_energy', 'wind_cons_change_pct',
                'wind_cons_change_twh', 'wind_consumption', 'wind_elec_per_capita', 'wind_electricity',
                'wind_energy_per_capita', 'wind_share_elec', 'wind_share_energy'
            ],
            'coal_prod_change_pct',
            cm.linear.viridis
        ],
        'agricultural-land': [
            [
                'Entity','Code','Year','Agricultural land'
            ],
            'Agricultural land',
            cm.linear.viridis
        ],
        'change-forest-area-share-total': [
            [
                'Entity','Code','Year','Conversion as share of forest area'
            ],
            'Conversion as share of forest area',
            cm.linear.viridis
        ],
        'co-emissions-per-capita': [
            [
                'Entity','Code','Year','Annual CO₂ emissions (per capita)'
            ],
            'Annual CO₂ emissions (per capita)',
            cm.linear.viridis
        ],
        'consumption-of-ozone-depleting-substances': [
            [
                'Entity','Code','Year','Consumption of controlled substance (zero-filled) - Chemical: All (Ozone-depleting)'
            ],
            'Consumption of controlled substance (zero-filled) - Chemical: All (Ozone-depleting)',
            cm.linear.viridis
        ],
        'fossil-fuel-primary-energy': [
            [
                'Entity','Code','Year','Fossil fuels (TWh)'
            ],
            'Fossil fuels (TWh)',
            cm.linear.viridis
        ],
        'fossil-fuels-per-capita': [
            [
                'Entity','Code','Year','Fossil fuels per capita (kWh)'
            ],
            'Fossil fuels per capita (kWh)',
            cm.linear.viridis
        ],
        'global-living-planet-index': [
            [
                'Entity','Code','Year','Living Planet Index','Upper CI','Lower CI'
            ],
            'Living Planet Index',
            cm.linear.viridis
        ]
    }