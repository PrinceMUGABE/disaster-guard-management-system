import numpy as np
from datetime import datetime, timedelta

class DisasterPreventionSystem:
    

    def __init__(self):
    # Define risk thresholds for different disasters common in Rwanda
        self.risk_thresholds = {
            'Drought': {
                'High': {
                    'rainfall_threshold': 0.5,
                    'humidity_threshold': 60,
                    'temperature_threshold': 25
                },
                'Medium': {
                    'rainfall_threshold': 1.0,
                    'humidity_threshold': 70,
                    'temperature_threshold': 23
                },
                'Low': {
                    'rainfall_threshold': 2.0,
                    'humidity_threshold': 80,
                    'temperature_threshold': 20
                }
            },
            'Landslide': {
                'High': {
                    'rainfall_threshold': 4.0,
                    'soil_moisture_threshold': 85,
                    'slope_threshold': 30
                },
                'Medium': {
                    'rainfall_threshold': 3.0,
                    'soil_moisture_threshold': 75,
                    'slope_threshold': 25
                },
                'Low': {
                    'rainfall_threshold': 2.0,
                    'soil_moisture_threshold': 65,
                    'slope_threshold': 20
                }
            },
            'Flood': {
                'High': {
                    'rainfall_threshold': 5.0,
                    'water_level_threshold': 2.0,
                    'ground_saturation': 90
                },
                'Medium': {
                    'rainfall_threshold': 3.5,
                    'water_level_threshold': 1.5,
                    'ground_saturation': 80
                },
                'Low': {
                    'rainfall_threshold': 2.5,
                    'water_level_threshold': 1.0,
                    'ground_saturation': 70
                }
            },
            'Storm': {
                'High': {
                    'wind_speed_threshold': 20.0,
                    'rainfall_threshold': 3.0,
                    'lightning_probability': 80
                },
                'Medium': {
                    'wind_speed_threshold': 15.0,
                    'rainfall_threshold': 2.0,
                    'lightning_probability': 60
                },
                'Low': {
                    'wind_speed_threshold': 10.0,
                    'rainfall_threshold': 1.0,
                    'lightning_probability': 40
                }
            },
            'Earthquake': {
                'High': {
                    'magnitude_threshold': 5.0,
                    'depth_threshold': 10,
                    'proximity_threshold': 50
                },
                'Medium': {
                    'magnitude_threshold': 4.0,
                    'depth_threshold': 20,
                    'proximity_threshold': 100
                },
                'Low': {
                    'magnitude_threshold': 3.0,
                    'depth_threshold': 30,
                    'proximity_threshold': 150
                }
            }
        }

        # Define prevention strategies for each disaster type
        self.prevention_strategies = {
            'Drought': {
                'immediate': [
                    'Implement water rationing',
                    'Deploy mobile water tanks',
                    'Issue farming advisory'
                ],
                'short_term': [
                    'Install water storage systems',
                    'Implement irrigation projects',
                    'Distribute drought-resistant seeds'
                ],
                'long_term': [
                    'Develop water harvesting infrastructure',
                    'Create community reservoirs',
                    'Implement sustainable agriculture programs'
                ]
            },
            'Landslide': {
                'immediate': [
                    'Evacuate high-risk areas',
                    'Set up emergency shelters',
                    'Install temporary drainage systems'
                ],
                'short_term': [
                    'Construct retaining walls',
                    'Improve drainage systems',
                    'Stabilize slopes with vegetation'
                ],
                'long_term': [
                    'Develop land use regulations',
                    'Implement reforestation programs',
                    'Build permanent protective structures'
                ]
            },
            'Flood': {
                'immediate': [
                    'Issue flood warnings',
                    'Activate emergency pumps',
                    'Prepare evacuation routes'
                ],
                'short_term': [
                    'Clear drainage systems',
                    'Build temporary flood barriers',
                    'Relocate vulnerable populations'
                ],
                'long_term': [
                    'Construct flood control systems',
                    'Develop wetland conservation',
                    'Implement flood-resistant housing'
                ]
            },
            'Storm': {
                'immediate': [
                    'Issue severe weather alerts',
                    'Secure loose structures',
                    'Prepare emergency response teams'
                ],
                'short_term': [
                    'Reinforce vulnerable buildings',
                    'Clear potential debris',
                    'Install lightning protection'
                ],
                'long_term': [
                    'Improve building codes',
                    'Develop storm shelter network',
                    'Create community warning systems'
                ]
            },
            'Earthquake': {
                'immediate': [
                    'Activate emergency response teams',
                    'Set up medical facilities',
                    'Conduct rapid building assessment'
                ],
                'short_term': [
                    'Retrofit vulnerable structures',
                    'Establish safety zones',
                    'Train emergency responders'
                ],
                'long_term': [
                    'Implement seismic building codes',
                    'Develop earthquake monitoring systems',
                    'Create public awareness programs'
                ]
            }
        }

        # Initialize regional risk factors specific to Rwanda
        def __init__(self):
            self.regional_risk_factors = {

    
    'Northern Province': {
            'Musanze': {
                'base_risks': {
                    'landslide_prone': True,
                    'volcanic_risk': True,
                    'altitude_factor': 1850
                },
                'sectors': {
                    'Busogo': {'specific_risk': 'high_volcanic'},
                    'Cyuve': {'specific_risk': 'moderate_landslide'},
                    'Gacaca': {'specific_risk': 'high_landslide'},
                    'Gashaki': {'specific_risk': 'moderate_volcanic'},
                    'Gataraga': {'specific_risk': 'high_volcanic'},
                    'Kimonyi': {'specific_risk': 'moderate_landslide'},
                    'Kinigi': {'specific_risk': 'high_volcanic'},
                    'Muhoza': {'specific_risk': 'moderate_landslide'},
                    'Muko': {'specific_risk': 'high_landslide'},
                    'Musanze': {'specific_risk': 'moderate_volcanic'},
                    'Nkotsi': {'specific_risk': 'high_landslide'},
                    'Nyange': {'specific_risk': 'moderate_landslide'},
                    'Remera': {'specific_risk': 'high_volcanic'},
                    'Rwaza': {'specific_risk': 'moderate_landslide'},
                    'Shingiro': {'specific_risk': 'high_volcanic'}
                }
            },
            'Burera': {
                'base_risks': {
                    'landslide_prone': True,
                    'volcanic_risk': True,
                    'altitude_factor': 2000
                },
                'sectors': {
                    'Bungwe': {'specific_risk': 'high_landslide'},
                    'Butaro': {'specific_risk': 'moderate_volcanic'},
                    'Cyanika': {'specific_risk': 'high_volcanic'},
                    'Cyeru': {'specific_risk': 'moderate_landslide'},
                    'Gahunga': {'specific_risk': 'high_landslide'},
                    'Gatebe': {'specific_risk': 'moderate_volcanic'},
                    'Gitovu': {'specific_risk': 'high_landslide'},
                    'Kagogo': {'specific_risk': 'moderate_landslide'},
                    'Kinoni': {'specific_risk': 'high_volcanic'},
                    'Kinyababa': {'specific_risk': 'moderate_landslide'},
                    'Kivuye': {'specific_risk': 'high_landslide'},
                    'Nemba': {'specific_risk': 'moderate_volcanic'},
                    'Rugarama': {'specific_risk': 'high_landslide'},
                    'Rugendabari': {'specific_risk': 'moderate_volcanic'},
                    'Ruhunde': {'specific_risk': 'high_volcanic'},
                    'Rusarabuye': {'specific_risk': 'moderate_landslide'},
                    'Rwerere': {'specific_risk': 'high_landslide'}
                }
            },
            'Gicumbi': {
                'base_risks': {
                    'landslide_prone': True,
                    'flood_risk': False,
                    'altitude_factor': 2200
                },
                'sectors': {
                    'Bukure': {'specific_risk': 'high_landslide'},
                    'Bwisige': {'specific_risk': 'moderate_landslide'},
                    'Byumba': {'specific_risk': 'high_landslide'},
                    'Cyumba': {'specific_risk': 'moderate_landslide'},
                    'Giti': {'specific_risk': 'high_landslide'},
                    'Kaniga': {'specific_risk': 'moderate_landslide'},
                    'Manyagiro': {'specific_risk': 'high_landslide'},
                    'Miyove': {'specific_risk': 'moderate_landslide'},
                    'Mugambi': {'specific_risk': 'high_landslide'},
                    'Mukarange': {'specific_risk': 'moderate_landslide'},
                    'Muko': {'specific_risk': 'high_landslide'},
                    'Mutete': {'specific_risk': 'moderate_landslide'},
                    'Nyamiyaga': {'specific_risk': 'high_landslide'},
                    'Nyankenke': {'specific_risk': 'moderate_landslide'},
                    'Rubaya': {'specific_risk': 'high_landslide'},
                    'Rukomo': {'specific_risk': 'moderate_landslide'},
                    'Rushaki': {'specific_risk': 'high_landslide'},
                    'Rutare': {'specific_risk': 'moderate_landslide'},
                    'Ruvune': {'specific_risk': 'high_landslide'},
                    'Rwamiko': {'specific_risk': 'moderate_landslide'},
                    'Shangasha': {'specific_risk': 'high_landslide'}
                }
            },
            'Gakenke': {
                'base_risks': {
                    'landslide_prone': True,
                    'flood_risk': True,
                    'altitude_factor': 1900
                },
                'sectors': {
                    'Busengo': {'specific_risk': 'high_landslide'},
                    'Coko': {'specific_risk': 'moderate_flood'},
                    'Cyabingo': {'specific_risk': 'high_landslide'},
                    'Gakenke': {'specific_risk': 'moderate_flood'},
                    'Gashenyi': {'specific_risk': 'high_landslide'},
                    'Janja': {'specific_risk': 'moderate_flood'},
                    'Kamubuga': {'specific_risk': 'high_landslide'},
                    'Karambo': {'specific_risk': 'moderate_flood'},
                    'Kivuruga': {'specific_risk': 'high_landslide'},
                    'Mataba': {'specific_risk': 'moderate_flood'},
                    'Minazi': {'specific_risk': 'high_landslide'},
                    'Mugunga': {'specific_risk': 'moderate_flood'},
                    'Muhondo': {'specific_risk': 'high_landslide'},
                    'Muyongwe': {'specific_risk': 'moderate_flood'},
                    'Muzo': {'specific_risk': 'high_landslide'},
                    'Nemba': {'specific_risk': 'moderate_flood'},
                    'Ruli': {'specific_risk': 'high_landslide'},
                    'Rusasa': {'specific_risk': 'moderate_flood'},
                    'Rushashi': {'specific_risk': 'high_landslide'}
                }
            },
            'Rulindo': {
                'base_risks': {
                    'landslide_prone': True,
                    'flood_risk': True,
                    'altitude_factor': 1800
                },
                'sectors': {
                    'Base': {'specific_risk': 'high_landslide'},
                    'Burega': {'specific_risk': 'moderate_flood'},
                    'Bushoki': {'specific_risk': 'high_landslide'},
                    'Buyoga': {'specific_risk': 'moderate_flood'},
                    'Cyinzuzi': {'specific_risk': 'high_landslide'},
                    'Cyungo': {'specific_risk': 'moderate_flood'},
                    'Kinihira': {'specific_risk': 'high_landslide'},
                    'Kisaro': {'specific_risk': 'moderate_flood'},
                    'Masoro': {'specific_risk': 'high_landslide'},
                    'Mbogo': {'specific_risk': 'moderate_flood'},
                    'Murambi': {'specific_risk': 'high_landslide'},
                    'Ngoma': {'specific_risk': 'moderate_flood'},
                    'Ntarabana': {'specific_risk': 'high_landslide'},
                    'Rukozo': {'specific_risk': 'moderate_flood'},
                    'Rusiga': {'specific_risk': 'high_landslide'},
                    'Shyorongi': {'specific_risk': 'moderate_flood'},
                    'Tumba': {'specific_risk': 'high_landslide'}
                }
            }
        },


                    
                    
                    
                    
                    
    'Eastern Province': {
        'Nyagatare': {
            'base_risks': {
                'drought_prone': True,
                'flood_risk': False,
                'altitude_factor': 1400
            },
            'sectors': {
                'Gatunda': {'specific_risk': 'high_drought'},
                'Karama': {'specific_risk': 'moderate_drought'},
                'Katabagemu': {'specific_risk': 'high_drought'},
                'Karangazi': {'specific_risk': 'moderate_drought'},
                'Kiyombe': {'specific_risk': 'high_drought'},
                'Matimba': {'specific_risk': 'moderate_drought'},
                'Mimuri': {'specific_risk': 'high_drought'},
                'Mukama': {'specific_risk': 'moderate_drought'},
                'Musheri': {'specific_risk': 'high_drought'},
                'Nyagatare': {'specific_risk': 'moderate_drought'},
                'Rukomo': {'specific_risk': 'high_drought'},
                'Rwempasha': {'specific_risk': 'moderate_drought'},
                'Rwimiyaga': {'specific_risk': 'high_drought'},
                'Tabagwe': {'specific_risk': 'moderate_drought'}
            }
        },
        'Gatsibo': {
            'base_risks': {
                'drought_prone': True,
                'flood_risk': False,
                'altitude_factor': 1350
            },
            'sectors': {
                'Gasange': {'specific_risk': 'high_drought'},
                'Gatsibo': {'specific_risk': 'moderate_drought'},
                'Gitoki': {'specific_risk': 'high_drought'},
                'Kabarore': {'specific_risk': 'moderate_drought'},
                'Kageyo': {'specific_risk': 'high_drought'},
                'Kiramuruzi': {'specific_risk': 'moderate_drought'},
                'Kiziguro': {'specific_risk': 'high_drought'},
                'Muhura': {'specific_risk': 'moderate_drought'},
                'Murambi': {'specific_risk': 'high_drought'},
                'Ngarama': {'specific_risk': 'moderate_drought'},
                'Remera': {'specific_risk': 'high_drought'},
                'Rwimbogo': {'specific_risk': 'moderate_drought'}
            }
        },
        'Kayonza': {
            'base_risks': {
                'drought_prone': True,
                'flood_risk': True,
                'altitude_factor': 1400
            },
            'sectors': {
                'Gahini': {'specific_risk': 'high_drought'},
                'Kabare': {'specific_risk': 'moderate_drought'},
                'Kabarondo': {'specific_risk': 'high_flood'},
                'Mukarange': {'specific_risk': 'moderate_drought'},
                'Murama': {'specific_risk': 'high_drought'},
                'Murundi': {'specific_risk': 'moderate_flood'},
                'Mwiri': {'specific_risk': 'high_drought'},
                'Ndego': {'specific_risk': 'moderate_flood'},
                'Nyamirama': {'specific_risk': 'moderate_drought'},
                'Rukara': {'specific_risk': 'high_drought'},
                'Ruramira': {'specific_risk': 'moderate_drought'}
            }
        },
        'Rwamagana': {
            'base_risks': {
                'drought_prone': True,
                'flood_risk': True,
                'altitude_factor': 1350
            },
            'sectors': {
                'Fumbwe': {'specific_risk': 'high_drought'},
                'Gahengeri': {'specific_risk': 'moderate_drought'},
                'Gishari': {'specific_risk': 'high_flood'},
                'Karenge': {'specific_risk': 'moderate_flood'},
                'Kigabiro': {'specific_risk': 'high_drought'},
                'Muhazi': {'specific_risk': 'moderate_flood'},
                'Mwulire': {'specific_risk': 'high_drought'},
                'Nyakaliro': {'specific_risk': 'moderate_flood'},
                'Nzige': {'specific_risk': 'high_drought'},
                'Rubona': {'specific_risk': 'moderate_drought'},
                'Rukara': {'specific_risk': 'high_flood'}
            }
        },
        'Kirehe': {
            'base_risks': {
                'drought_prone': True,
                'flood_risk': True,
                'altitude_factor': 1350
            },
            'sectors': {
                'Gahara': {'specific_risk': 'high_drought'},
                'Gatore': {'specific_risk': 'moderate_drought'},
                'Kigarama': {'specific_risk': 'high_flood'},
                'Kigina': {'specific_risk': 'moderate_flood'},
                'Kirehe': {'specific_risk': 'high_drought'},
                'Mahama': {'specific_risk': 'moderate_flood'},
                'Mpanga': {'specific_risk': 'high_drought'},
                'Musaza': {'specific_risk': 'moderate_drought'},
                'Mushikiri': {'specific_risk': 'high_drought'},
                'Nyamugari': {'specific_risk': 'moderate_drought'},
                'Nyarubuye': {'specific_risk': 'high_flood'}
            }
        },
        'Ngoma': {
            'base_risks': {
                'drought_prone': True,
                'flood_risk': True,
                'altitude_factor': 1400
            },
            'sectors': {
                'Gashanda': {'specific_risk': 'moderate_flood'},
                'Jarama': {'specific_risk': 'high_drought'},
                'Karembo': {'specific_risk': 'moderate_drought'},
                'Kazo': {'specific_risk': 'high_drought'},
                'Kibungo': {'specific_risk': 'moderate_drought'},
                'Mugesera': {'specific_risk': 'high_flood'},
                'Murama': {'specific_risk': 'moderate_drought'},
                'Mutenderi': {'specific_risk': 'high_drought'},
                'Remera': {'specific_risk': 'moderate_drought'},
                'Rukira': {'specific_risk': 'high_drought'},
                'Sake': {'specific_risk': 'moderate_flood'},
                'Zaza': {'specific_risk': 'high_drought'}
            }
        },
        'Bugesera': {
            'base_risks': {
                'drought_prone': True,
                'flood_risk': True,
                'altitude_factor': 1250
            },
            'sectors': {
                'Gashora': {'specific_risk': 'moderate_flood'},
                'Juru': {'specific_risk': 'high_drought'},
                'Kamabuye': {'specific_risk': 'moderate_flood'},
                'Mareba': {'specific_risk': 'high_drought'},
                'Mayange': {'specific_risk': 'moderate_drought'},
                'Musenyi': {'specific_risk': 'high_drought'},
                'Mwogo': {'specific_risk': 'moderate_flood'},
                'Ngeruka': {'specific_risk': 'moderate_drought'},
                'Ntarama': {'specific_risk': 'high_drought'},
                'Nyamata': {'specific_risk': 'moderate_flood'},
                'Rilima': {'specific_risk': 'high_drought'},
                'Ruhuha': {'specific_risk': 'moderate_drought'},
                'Shyara': {'specific_risk': 'moderate_flood'}
            }
        }
    },

                    
    'Western Province': {
        'Rubavu': {
            'base_risks': {
                'landslide_prone': True,
                'flood_risk': True,
                'altitude_factor': 1600
            },
            'sectors': {
                'Gisenyi': {'specific_risk': 'high_flood'},
                'Nyamyumba': {'specific_risk': 'moderate_landslide'},
                'Rugerero': {'specific_risk': 'high_landslide'},
                'Bugeshi': {'specific_risk': 'moderate_flood'},
                'Busasamana': {'specific_risk': 'high_flood'},
                'Cyanzarwe': {'specific_risk': 'moderate_landslide'},
                'Kanama': {'specific_risk': 'high_landslide'},
                'Kanzenze': {'specific_risk': 'moderate_flood'},
                'Mudende': {'specific_risk': 'high_landslide'},
                'Nyakiriba': {'specific_risk': 'moderate_flood'},
                'Nyundo': {'specific_risk': 'high_flood'},
                'Rubavu': {'specific_risk': 'moderate_landslide'}
            }
        },
        'Karongi': {
            'base_risks': {
                'landslide_prone': True,
                'flood_risk': True,
                'altitude_factor': 1400
            },
            'sectors': {
                'Bwishyura': {'specific_risk': 'high_landslide'},
                'Gishyita': {'specific_risk': 'moderate_flood'},
                'Gisovu': {'specific_risk': 'moderate_landslide'},
                'Gishari': {'specific_risk': 'moderate_flood'},
                'Murambi': {'specific_risk': 'high_landslide'},
                'Mubuga': {'specific_risk': 'moderate_flood'},
                'Mutuntu': {'specific_risk': 'moderate_landslide'},
                'Ruganda': {'specific_risk': 'low_flood'},
                'Rubengera': {'specific_risk': 'moderate_landslide'},
                'Rugabano': {'specific_risk': 'moderate_flood'},
                'Rwankuba': {'specific_risk': 'low_flood'},
                'Twumba': {'specific_risk': 'moderate_landslide'}
            }
        },
        'Rusizi': {
            'base_risks': {
                'landslide_prone': False,
                'flood_risk': True,
                'altitude_factor': 1350
            },
            'sectors': {
                'Bugarama': {'specific_risk': 'high_flood'},
                'Butare': {'specific_risk': 'moderate_flood'},
                'Gashonga': {'specific_risk': 'low_flood'},
                'Giheke': {'specific_risk': 'moderate_flood'},
                'Gihundwe': {'specific_risk': 'high_flood'},
                'Gitambi': {'specific_risk': 'moderate_flood'},
                'Kamembe': {'specific_risk': 'high_flood'},
                'Muganza': {'specific_risk': 'moderate_flood'},
                'Mururu': {'specific_risk': 'moderate_flood'},
                'Nkanka': {'specific_risk': 'low_flood'},
                'Nzahaha': {'specific_risk': 'low_flood'},
                'Nyakabuye': {'specific_risk': 'moderate_flood'},
                'Nkungu': {'specific_risk': 'moderate_flood'}
            }
        },
        'Nyamasheke': {
            'base_risks': {
                'landslide_prone': True,
                'flood_risk': True,
                'altitude_factor': 1500
            },
            'sectors': {
                'Bushekeri': {'specific_risk': 'moderate_landslide'},
                'Bushenge': {'specific_risk': 'high_flood'},
                'Cyato': {'specific_risk': 'low_flood'},
                'Gihombo': {'specific_risk': 'moderate_flood'},
                'Kagano': {'specific_risk': 'high_flood'},
                'Kanjongo': {'specific_risk': 'moderate_flood'},
                'Karambi': {'specific_risk': 'moderate_landslide'},
                'Karengera': {'specific_risk': 'low_landslide'},
                'Kirimbi': {'specific_risk': 'moderate_flood'},
                'Mahembe': {'specific_risk': 'low_flood'},
                'Rangiro': {'specific_risk': 'moderate_landslide'},
                'Shangi': {'specific_risk': 'moderate_flood'}
            }
        },
        'Ngororero': {
            'base_risks': {
                'landslide_prone': True,
                'flood_risk': False,
                'altitude_factor': 1800
            },
            'sectors': {
                'Bwira': {'specific_risk': 'high_landslide'},
                'Gatumba': {'specific_risk': 'moderate_landslide'},
                'Hindiro': {'specific_risk': 'moderate_landslide'},
                'Kabaya': {'specific_risk': 'high_landslide'},
                'Kageyo': {'specific_risk': 'moderate_landslide'},
                'Matyazo': {'specific_risk': 'low_landslide'},
                'Muhororo': {'specific_risk': 'moderate_landslide'},
                'Ndaro': {'specific_risk': 'low_landslide'},
                'Ngororero': {'specific_risk': 'moderate_landslide'},
                'Nyange': {'specific_risk': 'moderate_landslide'},
                'Sovu': {'specific_risk': 'low_landslide'}
            }
        },
        'Rutsiro': {
            'base_risks': {
                'landslide_prone': True,
                'flood_risk': True,
                'altitude_factor': 1600
            },
            'sectors': {
                'Boneza': {'specific_risk': 'moderate_flood'},
                'Gihango': {'specific_risk': 'high_landslide'},
                'Kigeyo': {'specific_risk': 'moderate_flood'},
                'Kivumu': {'specific_risk': 'high_landslide'},
                'Manihira': {'specific_risk': 'moderate_flood'},
                'Mukura': {'specific_risk': 'moderate_flood'},
                'Murunda': {'specific_risk': 'high_landslide'},
                'Musasa': {'specific_risk': 'moderate_flood'},
                'Mushonyi': {'specific_risk': 'moderate_flood'},
                'Nyabirasi': {'specific_risk': 'moderate_landslide'},
                'Ruhango': {'specific_risk': 'low_landslide'}
            }
        },
        'Nyabihu': {
            'base_risks': {
                'landslide_prone': True,
                'flood_risk': True,
                'altitude_factor': 2200
            },
            'sectors': {
                'Bigogwe': {'specific_risk': 'high_landslide'},
                'Jenda': {'specific_risk': 'moderate_flood'},
                'Jomba': {'specific_risk': 'moderate_landslide'},
                'Kabatwa': {'specific_risk': 'high_flood'},
                'Karago': {'specific_risk': 'moderate_flood'},
                'Kintobo': {'specific_risk': 'moderate_landslide'},
                'Mukamira': {'specific_risk': 'moderate_flood'},
                'Mulinga': {'specific_risk': 'moderate_landslide'},
                'Rambura': {'specific_risk': 'moderate_flood'},
                'Rurembo': {'specific_risk': 'high_landslide'},
                'Shyira': {'specific_risk': 'moderate_flood'}
            }
        }
    },

                
                
                
    'Southern Province': {
        'Huye': {
            'base_risks': {
                'flood_prone': True,
                'drought_risk': True,
                'altitude_factor': 1700
            },
            'sectors': {
                'Gishamvu': {'specific_risk': 'high_flood'},
                'Karama': {'specific_risk': 'moderate_drought'},
                'Kigoma': {'specific_risk': 'moderate_drought'},
                'Kinazi': {'specific_risk': 'high_drought'},
                'Maraba': {'specific_risk': 'high_drought'},
                'Mbazi': {'specific_risk': 'high_flood'},
                'Mukura': {'specific_risk': 'moderate_flood'},
                'Ngoma': {'specific_risk': 'high_flood'},
                'Ruhashya': {'specific_risk': 'moderate_drought'},
                'Rusatira': {'specific_risk': 'moderate_drought'},
                'Rwaniro': {'specific_risk': 'high_drought'},
                'Simbi': {'specific_risk': 'moderate_flood'},
                'Tumba': {'specific_risk': 'moderate_flood'}
            }
        },
        'Muhanga': {
            'base_risks': {
                'flood_prone': True,
                'drought_risk': False,
                'altitude_factor': 1650
            },
            'sectors': {
                'Cyeza': {'specific_risk': 'moderate_flood'},
                'Kabacuzi': {'specific_risk': 'low_drought'},
                'Kibangu': {'specific_risk': 'moderate_flood'},
                'Kiyumba': {'specific_risk': 'moderate_flood'},
                'Muhanga': {'specific_risk': 'high_flood'},
                'Mushishiro': {'specific_risk': 'moderate_drought'},
                'Nyabinoni': {'specific_risk': 'low_drought'},
                'Nyamabuye': {'specific_risk': 'moderate_flood'},
                'Nyarusange': {'specific_risk': 'low_drought'},
                'Rongi': {'specific_risk': 'moderate_flood'},
                'Rugendabari': {'specific_risk': 'low_drought'},
                'Shyogwe': {'specific_risk': 'moderate_flood'}
            }
        },
        'Nyanza': {
            'base_risks': {
                'flood_prone': True,
                'drought_risk': True,
                'altitude_factor': 1550
            },
            'sectors': {
                'Busasamana': {'specific_risk': 'moderate_drought'},
                'Busoro': {'specific_risk': 'low_drought'},
                'Cyabakamyi': {'specific_risk': 'moderate_flood'},
                'Kibirizi': {'specific_risk': 'low_drought'},
                'Kigoma': {'specific_risk': 'high_drought'},
                'Mukingo': {'specific_risk': 'moderate_flood'},
                'Muyira': {'specific_risk': 'low_drought'},
                'Ntyazo': {'specific_risk': 'high_drought'},
                'Nyagisozi': {'specific_risk': 'low_flood'},
                'Rwabicuma': {'specific_risk': 'moderate_drought'}
            }
        },
        'Ruhango': {
            'base_risks': {
                'flood_prone': True,
                'drought_risk': True,
                'altitude_factor': 1500
            },
            'sectors': {
                'Bweramana': {'specific_risk': 'moderate_flood'},
                'Byimana': {'specific_risk': 'low_drought'},
                'Kabagari': {'specific_risk': 'moderate_drought'},
                'Kinazi': {'specific_risk': 'moderate_flood'},
                'Kinihira': {'specific_risk': 'low_drought'},
                'Mbuye': {'specific_risk': 'moderate_drought'},
                'Mwendo': {'specific_risk': 'low_drought'},
                'Ntongwe': {'specific_risk': 'moderate_flood'},
                'Ruhango': {'specific_risk': 'moderate_flood'}
            }
        },
        'Nyamagabe': {
            'base_risks': {
                'flood_prone': True,
                'drought_risk': True,
                'altitude_factor': 1900
            },
            'sectors': {
                'Buruhukiro': {'specific_risk': 'high_flood'},
                'Cyanika': {'specific_risk': 'moderate_flood'},
                'Gasaka': {'specific_risk': 'high_drought'},
                'Gatare': {'specific_risk': 'moderate_drought'},
                'Kaduha': {'specific_risk': 'moderate_flood'},
                'Kamegeri': {'specific_risk': 'high_flood'},
                'Kibumbwe': {'specific_risk': 'moderate_flood'},
                'Kibumba': {'specific_risk': 'low_drought'},
                'Mbazi': {'specific_risk': 'moderate_flood'},
                'Musebeya': {'specific_risk': 'high_drought'},
                'Musange': {'specific_risk': 'moderate_flood'},
                'Nyabimata': {'specific_risk': 'low_drought'},
                'Uwinkingi': {'specific_risk': 'moderate_drought'}
            }
        },
        'Nyaruguru': {
            'base_risks': {
                'flood_prone': True,
                'drought_risk': False,
                'altitude_factor': 2100
            },
            'sectors': {
                'Busanze': {'specific_risk': 'moderate_flood'},
                'Cyahinda': {'specific_risk': 'low_drought'},
                'Kibeho': {'specific_risk': 'moderate_flood'},
                'Kivu': {'specific_risk': 'low_drought'},
                'Mata': {'specific_risk': 'moderate_flood'},
                'Muganza': {'specific_risk': 'moderate_flood'},
                'Munini': {'specific_risk': 'moderate_flood'},
                'Ngoma': {'specific_risk': 'high_flood'},
                'Ngera': {'specific_risk': 'low_flood'},
                'Nyabimata': {'specific_risk': 'moderate_flood'},
                'Ruheru': {'specific_risk': 'moderate_drought'},
                'Ruramba': {'specific_risk': 'moderate_flood'}
            }
        }
    },

                    
                    
    'Kigali City': {
                    'Nyarugenge': {
                        'base_risks': {
                            'flood_prone': True,
                            'urban_risk': True,
                            'altitude_factor': 1567
                        },
                        'sectors': {
                            'Gitega': {'specific_risk': 'high_urban_flood'},
                            'Kanyinya': {'specific_risk': 'moderate_urban_flood'},
                            'Kigali': {'specific_risk': 'high_urban_flood'},
                            'Kimisagara': {'specific_risk': 'moderate_urban_flood'},
                            'Mageragere': {'specific_risk': 'high_urban_flood'},
                            'Muhima': {'specific_risk': 'moderate_urban_flood'},
                            'Nyakabanda': {'specific_risk': 'high_urban_flood'},
                            'Nyamirambo': {'specific_risk': 'moderate_urban_flood'},
                            'Nyarugenge': {'specific_risk': 'high_urban_flood'},
                            'Rwezamenyo': {'specific_risk': 'moderate_urban_flood'}
                        }
                    },
                    'Gasabo': {
                        'base_risks': {
                            'flood_prone': True,
                            'urban_risk': True,
                            'altitude_factor': 1500
                        },
                        'sectors': {
                            'Bumbogo': {'specific_risk': 'moderate_urban_flood'},
                            'Gatsata': {'specific_risk': 'high_urban_flood'},
                            'Gisozi': {'specific_risk': 'moderate_urban_flood'},
                            'Jali': {'specific_risk': 'moderate_urban_flood'},
                            'Kacyiru': {'specific_risk': 'high_urban_flood'},
                            'Kimironko': {'specific_risk': 'moderate_urban_flood'},
                            'Kinyinya': {'specific_risk': 'high_urban_flood'},
                            'Ndera': {'specific_risk': 'moderate_urban_flood'},
                            'Nduba': {'specific_risk': 'moderate_urban_flood'},
                            'Remera': {'specific_risk': 'high_urban_flood'},
                            'Rusororo': {'specific_risk': 'moderate_urban_flood'},
                            'Rutunga': {'specific_risk': 'moderate_urban_flood'}
                        }
                    },
                    'Kicukiro': {
                        'base_risks': {
                            'flood_prone': True,
                            'urban_risk': True,
                            'altitude_factor': 1450
                        },
                        'sectors': {
                            'Gahanga': {'specific_risk': 'moderate_urban_flood'},
                            'Gatenga': {'specific_risk': 'high_urban_flood'},
                            'Gikondo': {'specific_risk': 'moderate_urban_flood'},
                            'Kagarama': {'specific_risk': 'moderate_urban_flood'},
                            'Kanombe': {'specific_risk': 'high_urban_flood'},
                            'Kicukiro': {'specific_risk': 'high_urban_flood'},
                            'Masaka': {'specific_risk': 'moderate_urban_flood'},
                            'Niboye': {'specific_risk': 'moderate_urban_flood'},
                            'Nyarugunga': {'specific_risk': 'high_urban_flood'}
                        }
                    }
                }
        
}
        
        
    def analyze_prediction(self, prediction_data):
        """Analyzes prediction data and generates prevention strategies"""
        disaster_type = prediction_data['Most Likely Disaster']
        risk_level = prediction_data['Risk Level']
        
        # Create prevention plan based on prediction
        prevention_plan = {
            'location': {
                'district': prediction_data['District'],
                'sector': prediction_data['Sector']
            },
            'current_conditions': {
                'temperature': prediction_data['Temperature'],
                'wind_speed': prediction_data['Wind Speed'],
                'humidity': prediction_data['Humidity'],
                'rainfall': prediction_data['Rainfall'],
                'soil_type': prediction_data['Soil Type']
            },
            'risk_assessment': {
                'level': risk_level,
                'confidence': prediction_data['Confidence Score']
            },
            'prevention_strategies': self.generate_prevention_strategies(disaster_type, prediction_data),
            'timeline': self.generate_timeline(),
            'resource_requirements': self.calculate_resource_requirements(disaster_type, risk_level)
        }
        
        return prevention_plan

    def generate_prevention_strategies(self, disaster_type, prediction_data):
        """Generates specific prevention strategies based on disaster type and conditions"""
        if disaster_type == 'Drought':
            return {
                'immediate_actions': [
                    {
                        'action': 'Water Conservation Alert',
                        'description': 'Issue immediate water conservation guidelines to the community',
                        'priority': 'High',
                        'responsible_entity': 'Local Water Authority'
                    },
                    {
                        'action': 'Agricultural Advisory',
                        'description': 'Provide guidance on drought-resistant farming practices',
                        'priority': 'High',
                        'responsible_entity': 'Agricultural Extension Officers'
                    }
                ],
                'short_term_actions': [
                    {
                        'action': 'Water Storage Implementation',
                        'description': 'Deploy water storage solutions and establish water points',
                        'priority': 'High',
                        'responsible_entity': 'District Infrastructure Team'
                    },
                    {
                        'action': 'Irrigation System Check',
                        'description': 'Inspect and repair irrigation systems',
                        'priority': 'Medium',
                        'responsible_entity': 'Agricultural Department'
                    }
                ],
                'long_term_actions': [
                    {
                        'action': 'Infrastructure Development',
                        'description': 'Develop long-term water infrastructure and storage facilities',
                        'priority': 'Medium',
                        'responsible_entity': 'District Planning Department'
                    },
                    {
                        'action': 'Community Training',
                        'description': 'Implement community training programs on water conservation',
                        'priority': 'Medium',
                        'responsible_entity': 'Red Cross Training Team'
                    }
                ]
            }
        elif disaster_type == 'Storm':
            return {
                'immediate_actions': [
                    {
                        'action': 'Storm Warning Alert',
                        'description': 'Issue immediate storm warning to affected communities',
                        'priority': 'High',
                        'responsible_entity': 'Meteorological Department'
                    },
                    {
                        'action': 'Emergency Shelter Activation',
                        'description': 'Prepare and activate emergency storm shelters',
                        'priority': 'High',
                        'responsible_entity': 'Emergency Response Team'
                    }
                ],
                'short_term_actions': [
                    {
                        'action': 'Infrastructure Protection',
                        'description': 'Secure vulnerable infrastructure and clear potential hazards',
                        'priority': 'High',
                        'responsible_entity': 'District Infrastructure Team'
                    },
                    {
                        'action': 'Emergency Supply Distribution',
                        'description': 'Distribute emergency supplies and equipment',
                        'priority': 'Medium',
                        'responsible_entity': 'Relief Coordination Team'
                    }
                ],
                'long_term_actions': [
                    {
                        'action': 'Storm-Resistant Infrastructure',
                        'description': 'Develop and implement storm-resistant building standards',
                        'priority': 'Medium',
                        'responsible_entity': 'District Planning Department'
                    },
                    {
                        'action': 'Early Warning System Enhancement',
                        'description': 'Upgrade storm detection and warning systems',
                        'priority': 'Medium',
                        'responsible_entity': 'Meteorological Department'
                    }
                ]
            }
        elif disaster_type == 'Flood':
            return {
                'immediate_actions': [
                    {
                        'action': 'Flood Warning Alert',
                        'description': 'Issue immediate flood warnings and evacuation notices',
                        'priority': 'High',
                        'responsible_entity': 'Meteorological Department'
                    },
                    {
                        'action': 'Emergency Evacuation',
                        'description': 'Evacuate communities in high-risk flood areas',
                        'priority': 'High',
                        'responsible_entity': 'Emergency Response Team'
                    }
                ],
                'short_term_actions': [
                    {
                        'action': 'Drainage System Maintenance',
                        'description': 'Clear and maintain drainage systems to prevent blockages',
                        'priority': 'High',
                        'responsible_entity': 'District Infrastructure Team'
                    },
                    {
                        'action': 'Flood Barrier Deployment',
                        'description': 'Deploy temporary flood barriers in vulnerable areas',
                        'priority': 'Medium',
                        'responsible_entity': 'Relief Coordination Team'
                    }
                ],
                'long_term_actions': [
                    {
                        'action': 'Flood-Resilient Infrastructure',
                        'description': 'Construct flood-resilient infrastructure and improve urban planning',
                        'priority': 'Medium',
                        'responsible_entity': 'District Planning Department'
                    },
                    {
                        'action': 'Reforestation Initiatives',
                        'description': 'Promote reforestation to reduce runoff and stabilize soil',
                        'priority': 'Medium',
                        'responsible_entity': 'Environmental Conservation Team'
                    }
                ]
            }
        elif disaster_type == 'Landslide':
            return {
                'immediate_actions': [
                    {
                        'action': 'Landslide Risk Alert',
                        'description': 'Issue warnings to communities in landslide-prone areas',
                        'priority': 'High',
                        'responsible_entity': 'Geological Survey Department'
                    },
                    {
                        'action': 'Evacuation and Relocation',
                        'description': 'Relocate families living in high-risk areas',
                        'priority': 'High',
                        'responsible_entity': 'Emergency Response Team'
                    }
                ],
                'short_term_actions': [
                    {
                        'action': 'Slope Stabilization',
                        'description': 'Reinforce vulnerable slopes with retaining walls and vegetation',
                        'priority': 'High',
                        'responsible_entity': 'District Infrastructure Team'
                    },
                    {
                        'action': 'Drainage Improvement',
                        'description': 'Ensure proper drainage to reduce soil saturation',
                        'priority': 'Medium',
                        'responsible_entity': 'Environmental Conservation Team'
                    }
                ],
                'long_term_actions': [
                    {
                        'action': 'Land Use Planning',
                        'description': 'Enforce zoning regulations to avoid construction in landslide-prone areas',
                        'priority': 'Medium',
                        'responsible_entity': 'District Planning Department'
                    },
                    {
                        'action': 'Community Education',
                        'description': 'Educate communities about landslide risks and prevention measures',
                        'priority': 'Medium',
                        'responsible_entity': 'Red Cross Training Team'
                    }
                ]
            }
        elif disaster_type == 'Earthquake':
                return {
                    'immediate_actions': [
                        {
                            'action': 'Earthquake Warning Alert',
                            'description': 'Issue alerts and provide safety guidelines immediately',
                            'priority': 'High',
                            'responsible_entity': 'Seismological Monitoring Agency'
                        },
                        {
                            'action': 'Emergency Shelter Setup',
                            'description': 'Prepare emergency shelters for displaced individuals',
                            'priority': 'High',
                            'responsible_entity': 'Emergency Response Team'
                        }
                    ],
                    'short_term_actions': [
                        {
                            'action': 'Structural Assessment',
                            'description': 'Inspect and reinforce critical infrastructure for earthquake resilience',
                            'priority': 'High',
                            'responsible_entity': 'District Infrastructure Team'
                        },
                        {
                            'action': 'Emergency Supply Preparation',
                            'description': 'Distribute emergency supplies and first aid kits',
                            'priority': 'Medium',
                            'responsible_entity': 'Relief Coordination Team'
                        }
                    ],
                    'long_term_actions': [
                        {
                            'action': 'Earthquake-Resistant Construction',
                            'description': 'Adopt earthquake-resistant building standards',
                            'priority': 'Medium',
                            'responsible_entity': 'District Planning Department'
                        },
                        {
                            'action': 'Seismic Monitoring Enhancement',
                            'description': 'Upgrade seismic monitoring and early warning systems',
                            'priority': 'Medium',
                            'responsible_entity': 'Seismological Monitoring Agency'
                        }
                    ]
                }
        return {}


    def generate_prevention_strategies(self, disaster_type, prediction_data):
            """Generates specific prevention strategies based on disaster type and conditions"""
            if disaster_type == 'Drought':
                return {
                    'immediate_actions': [
                        {
                            'action': 'Water Conservation Alert',
                            'description': 'Issue immediate water conservation guidelines to the community',
                            'priority': 'High',
                            'responsible_entity': 'Local Water Authority'
                        },
                        {
                            'action': 'Agricultural Advisory',
                            'description': 'Provide guidance on drought-resistant farming practices',
                            'priority': 'High',
                            'responsible_entity': 'Agricultural Extension Officers'
                        }
                    ],
                    'short_term_actions': [
                        {
                            'action': 'Water Storage Implementation',
                            'description': 'Deploy water storage solutions and establish water points',
                            'priority': 'High',
                            'responsible_entity': 'District Infrastructure Team'
                        },
                        {
                            'action': 'Irrigation System Check',
                            'description': 'Inspect and repair irrigation systems',
                            'priority': 'Medium',
                            'responsible_entity': 'Agricultural Department'
                        }
                    ],
                    'long_term_actions': [
                        {
                            'action': 'Infrastructure Development',
                            'description': 'Develop long-term water infrastructure and storage facilities',
                            'priority': 'Medium',
                            'responsible_entity': 'District Planning Department'
                        },
                        {
                            'action': 'Community Training',
                            'description': 'Implement community training programs on water conservation',
                            'priority': 'Medium',
                            'responsible_entity': 'Red Cross Training Team'
                        }
                    ]
                }
            # Add more disaster types as needed
            return {}

    def generate_timeline(self):
            """Generates implementation timeline for prevention strategies"""
            current_date = datetime.now()
            return {
                'immediate': current_date.strftime('%Y-%m-%d'),
                'short_term': (current_date + timedelta(days=7)).strftime('%Y-%m-%d'),
                'long_term': (current_date + timedelta(days=30)).strftime('%Y-%m-%d')
            }

    def calculate_resource_requirements(self, disaster_type, risk_level):
        
            if disaster_type == 'Drought':
                return {
                    'personnel': {
                        'agricultural_officers': 5,
                        'water_engineers': 3,
                        'community_trainers': 8,
                        'irrigation_specialists': 4,
                        'soil_conservation_experts': 3
                    },
                    'equipment': {
                        'water_storage_tanks': 10,
                        'irrigation_kits': 50,
                        'water_quality_testing_kits': 20,
                        'soil_moisture_sensors': 30,
                        'mobile_water_pumps': 5
                    },
                    'estimated_budget': self._calculate_budget(risk_level)
                }
            
            elif disaster_type == 'Landslide':
                    return {
                        'personnel': {
                            'geologists': 3,
                            'soil_engineers': 4,
                            'evacuation_coordinators': 6,
                            'rescue_teams': 8,
                            'construction_experts': 5
                        },
                        'equipment': {
                            'soil_monitoring_devices': 15,
                            'evacuation_vehicles': 4,
                            'earth_moving_equipment': 3,
                            'emergency_shelters': 6,
                            'geological_survey_tools': 10,
                            'drainage_system_equipment': 8
                        },
                        'estimated_budget': self._calculate_budget(risk_level)
                    }
                
            elif disaster_type == 'Flood':
                    return {
                        'personnel': {
                            'hydrologists': 3,
                            'flood_control_engineers': 4,
                            'emergency_responders': 10,
                            'evacuation_teams': 6,
                            'medical_personnel': 8
                        },
                        'equipment': {
                            'water_pumps': 12,
                            'flood_barriers': 30,
                            'rescue_boats': 5,
                            'water_level_sensors': 20,
                            'emergency_communication_systems': 4,
                            'water_purification_units': 6
                        },
                        'estimated_budget': self._calculate_budget(risk_level)
                    }
                
            elif disaster_type == 'Storm':
                
                return {
                        'personnel': {
                            'emergency_responders': 10,
                            'meteorologists': 2,
                            'community_coordinators': 5,
                            'power_restoration_teams': 6,
                            'debris_removal_crews': 8
                        },
                        'equipment': {
                            'emergency_shelters': 5,
                            'weather_monitoring_stations': 3,
                            'emergency_communication_systems': 2,
                            'power_generators': 8,
                            'debris_removal_vehicles': 4,
                            'early_warning_sirens': 10
                        },
                        'estimated_budget': self._calculate_budget(risk_level)
                    }
                
            elif disaster_type == 'Earthquake':
                return {
                    'personnel': {
                        'seismologists': 2,
                        'structural_engineers': 4,
                        'search_rescue_teams': 12,
                        'medical_emergency_teams': 8,
                        'building_inspectors': 6
                    },
                    'equipment': {
                        'seismic_monitoring_devices': 8,
                        'rescue_equipment': 15,
                        'mobile_medical_units': 4,
                        'emergency_shelters': 10,
                        'structural_assessment_tools': 12,
                        'heavy_lifting_equipment': 5
                    },
                    'estimated_budget': self._calculate_budget(risk_level)
                }
            
            elif disaster_type == 'Volcanic':  # For regions near Virunga volcanoes
                return {
                    'personnel': {
                        'volcanologists': 3,
                        'evacuation_coordinators': 8,
                        'emergency_responders': 12,
                        'geological_surveyors': 4,
                        'air_quality_monitors': 3
                    },
                    'equipment': {
                        'gas_monitoring_devices': 10,
                        'evacuation_vehicles': 8,
                        'respiratory_protection_kits': 100,
                        'seismic_sensors': 15,
                        'emergency_communication_systems': 5,
                        'mobile_air_quality_stations': 6
                    },
                    'estimated_budget': self._calculate_budget(risk_level)
                }

            # Default return for any other disaster types
            return {
                'personnel': {
                    'emergency_responders': 5,
                    'community_coordinators': 3,
                    'medical_personnel': 4,
                    'logistics_coordinators': 2
                },
                'equipment': {
                    'emergency_kits': 20,
                    'communication_devices': 10,
                    'first_aid_supplies': 30,
                    'temporary_shelters': 5
                },
                'estimated_budget': self._calculate_budget(risk_level)
            }
            
            
            
            
    def _calculate_budget(self, risk_level):
            """Calculate budget based on risk level"""
            base_budget = 50000  # Base budget in USD
            risk_multipliers = {'High': 2.0, 'Medium': 1.5, 'Low': 1.0}
            return base_budget * risk_multipliers.get(risk_level, 1.0)

    def monitor_implementation(self, prevention_plan):
            """Monitors the implementation of prevention strategies"""
            return {
                'status': 'Active',
                'completed_actions': [],
                'pending_actions': prevention_plan['prevention_strategies'],
                'next_review_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            }

        