"""File that shuffles fairies locations."""

import random

from randomizer.Lists.FairyLocations import fairy_locations
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.Location import LocationList
from randomizer.LogicClasses import LocationLogic

import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.HideoutHelm
import randomizer.LogicFiles.JungleJapes

class FairyPlacementInfo:
    """Stores information regarding the internal memory table of fairies."""

    def __init__(self, location: Locations, level: Levels, internal_level_index: int):
        """Initialize with given data."""
        self.location = location
        self.level = level
        self.internal_level_index = internal_level_index

def ShuffleFairyLocations(spoiler: Spoiler):
    spoiler.fairy_locations = {}
    spoiler.fairy_locations_human = {}
    spoiler.fairy_data_table = [None]*20
    level_to_enum = {
        Levels.DKIsles: randomizer.LogicFiles.DKIsles.LogicRegions,
        Levels.JungleJapes: randomizer.LogicFiles.JungleJapes.LogicRegions,
        Levels.AngryAztec: randomizer.LogicFiles.AngryAztec.LogicRegions,
        Levels.FranticFactory: randomizer.LogicFiles.FranticFactory.LogicRegions,
        Levels.GloomyGalleon: randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        Levels.FungiForest: randomizer.LogicFiles.FungiForest.LogicRegions,
        Levels.CrystalCaves: randomizer.LogicFiles.CrystalCaves.LogicRegions,
        Levels.CreepyCastle: randomizer.LogicFiles.CreepyCastle.LogicRegions,
        Levels.HideoutHelm: randomizer.LogicFiles.HideoutHelm.LogicRegions,
    }
    if spoiler.settings.random_fairies:
        fairy_data_table = [
            # HAS to remain in this order. DO NOT REORDER
            FairyPlacementInfo(Locations.JapesBananaFairyRambiCave, Levels.JungleJapes, 0),
            FairyPlacementInfo(Locations.JapesBananaFairyLankyCave, Levels.JungleJapes, 1),
            FairyPlacementInfo(Locations.AztecBananaFairyLlamaTemple, Levels.AngryAztec, 0),
            FairyPlacementInfo(Locations.AztecBananaFairyTinyTemple, Levels.AngryAztec, 1),
            FairyPlacementInfo(Locations.FactoryBananaFairybyFunky, Levels.FranticFactory, 0),
            FairyPlacementInfo(Locations.FactoryBananaFairybyCounting, Levels.FranticFactory, 1),
            FairyPlacementInfo(Locations.GalleonBananaFairybyCranky, Levels.GloomyGalleon, 0),
            FairyPlacementInfo(Locations.GalleonBananaFairy5DoorShip, Levels.GloomyGalleon, 1),
            FairyPlacementInfo(Locations.CavesBananaFairyIgloo, Levels.CrystalCaves, 0),
            FairyPlacementInfo(Locations.CavesBananaFairyCabin, Levels.CrystalCaves, 1),
            FairyPlacementInfo(Locations.ForestBananaFairyRafters, Levels.FungiForest, 0),
            FairyPlacementInfo(Locations.ForestBananaFairyThornvines, Levels.FungiForest, 1),
            FairyPlacementInfo(Locations.CastleBananaFairyBallroom, Levels.CreepyCastle, 0),
            FairyPlacementInfo(Locations.CastleBananaFairyTree, Levels.CreepyCastle, 1),
            FairyPlacementInfo(Locations.IslesBananaFairyFactoryLobby, Levels.DKIsles, 0),
            FairyPlacementInfo(Locations.IslesBananaFairyForestLobby, Levels.DKIsles, 1),
            FairyPlacementInfo(Locations.IslesBananaFairyIsland, Levels.DKIsles, 2),
            FairyPlacementInfo(Locations.IslesBananaFairyCrocodisleIsle, Levels.DKIsles, 3),
            FairyPlacementInfo(Locations.HelmBananaFairy1, Levels.HideoutHelm, 0),
            FairyPlacementInfo(Locations.HelmBananaFairy2, Levels.HideoutHelm, 1),
        ]
        for level in fairy_locations:
            pick_size = 2
            if level == Levels.DKIsles:
                pick_size = 4
            selection = random.sample(list(range(len(fairy_locations[level]))), pick_size)
            human_selection = [fairy_locations[level][x].name for x in selection]
            spoiler.fairy_locations[level] = selection.copy()
            spoiler.fairy_locations_human[level.name] = "<br>".join(human_selection)
            # Placement into the table format, placement into logic
            vacant_slots = list(range(pick_size))
            for x in selection:
                slot = fairy_locations[level][x].natural_index
                if slot >= 0:
                    vacant_slots = [y for y in vacant_slots if y != slot]
            for x in selection:
                slot = fairy_locations[level][x].natural_index
                if slot < 0:
                    slot = vacant_slots.pop()
                for index, data in enumerate(fairy_data_table):
                    if data.level == level and data.internal_level_index == slot:
                        # Data array in ROM
                        spoiler.fairy_data_table[index] = {
                            "fairy_index": x,
                            "level": level,
                            "flag": LocationList[data.location].default_mapid_data[0].flag
                        }
                        # Logic
                        # Remove old from logic
                        for logic_region in level_to_enum[level]:
                            level_to_enum[level][logic_region].locations = [loc for loc in level_to_enum[level][logic_region].locations if loc.id != data.location]
                        # Re-insert into logic
                        new_region = fairy_locations[level][x].region
                        level_to_enum[level][new_region].locations.append(LocationLogic(data.location, fairy_locations[level][x].logic))
                                