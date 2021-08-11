class Maps:

    @staticmethod
    def get_preset(preset):
        if preset == 'basic_map':
            return Maps.basicmap()
        elif preset == 'three_countries_map':
            return Maps.three_countries_map()
        elif preset == 'one_tile_map':
            return Maps.one_tile_map()
        elif preset == 'two_tile_map':
            return Maps.two_tile_map()
        else:
            assert False, 'MAP PRESET NAME NOT VALID'

            
    @staticmethod
    def one_tile_map():
        map_preset = [
            ('P0','PLAINS',[]), #P0
        ]
        return map_preset
    
    @staticmethod
    def two_tile_map():
        map_preset = [
            ('P0','PLAINS',[1]), #P0
            ('P1','FARMLANDS',[0]), #P0
        ]
        return map_preset
            
    @staticmethod
    def basicmap():
        map_preset = [
            ('P0','FARMLANDS',[1,2]), #P0
            ('P1','PLAINS',[0,2,3]), #P1
            ('P2','PLAINS',[0,1,3,4]), #P2
            ('P3','HILLS',[1,2,4]), #P3
            ('P4','MOUNTAINS',[2,3]), #P4
        ]
        return map_preset

    @staticmethod
    def three_countries_map():
        map_preset = [
            ('A1','FARMLANDS',[1,2,3,6]), #A1 0
            ('A2','PLAINS',[0,2]), #A2   1
            ('A3','PLAINS',[0,1]), #A3 2
            ('B1','PLAINS',[4,5,0,6]), #B1     3
            ('B2','PLAINS',[3,5]), #B2   4
            ('B3','HILLS',[3,4]), #B3  5          
            ('C1','PLAINS',[7,8,0,3]), #C1     6
            ('C2','HILLS',[6,8]), #C2    7
            ('C3','MOUNTAINS',[6,7]), #C3   8
        ]

        return map_preset
    