"""Randomize Price Locations."""
from randomizer.Enums.Items import Items
from randomizer.Enums.Settings import MoveRando, RandomPrices
from randomizer.Patching.Patcher import ROM, LocalROM


def randomize_prices(spoiler):
    """Write prices to ROM variable space based on settings."""
    if spoiler.settings.random_prices != RandomPrices.vanilla:
        ROM_COPY = LocalROM()
        varspaceOffset = spoiler.settings.rom_data
        ROM_COPY.seek(varspaceOffset + 0x35)
        # /* 0x035 */ char price_rando_on; // 0 = Price Randomizer off, 1 = On
        if spoiler.settings.random_prices != RandomPrices.vanilla:
            ROM_COPY.write(1)
        else:
            ROM_COPY.write(0)
        progressive_items = {Items.ProgressiveAmmoBelt: 2, Items.ProgressiveInstrumentUpgrade: 3, Items.ProgressiveSlam: 2}
        for item in progressive_items:
            if item not in spoiler.settings.prices:
                spoiler.settings.prices[item] = []
            length = progressive_items[item]
            if len(spoiler.settings.prices[item]) < length:
                diff = length - len(spoiler.settings.prices[item])
                for d in range(diff):
                    spoiler.settings.prices[item].append(0)
        ROM_COPY.seek(varspaceOffset + 0x45)
        ROM_COPY.write(spoiler.settings.prices[Items.ProgressiveSlam][0])
        ROM_COPY.write(spoiler.settings.prices[Items.ProgressiveSlam][1])

        ROM_COPY.seek(varspaceOffset + 0x53)
        ROM_COPY.write(spoiler.settings.prices[Items.ProgressiveAmmoBelt][0])
        ROM_COPY.write(spoiler.settings.prices[Items.ProgressiveAmmoBelt][1])
        ROM_COPY.write(spoiler.settings.prices[Items.ProgressiveInstrumentUpgrade][0])
        ROM_COPY.write(spoiler.settings.prices[Items.ProgressiveInstrumentUpgrade][1])
        ROM_COPY.write(spoiler.settings.prices[Items.ProgressiveInstrumentUpgrade][2])
