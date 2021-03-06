"""Test reading MAP files from Rainbow Six (1998)"""
import logging
import unittest
from os import path

from FileUtilities.Settings import load_settings
from FileUtilities.DirectoryUtils import gather_files_in_path
from RainbowFileReaders import MAPLevelReader
from RainbowFileReaders.R6Constants import RSEGameVersions

TEST_SETTINGS_FILE = "test_settings.json"

logging.basicConfig(level=logging.CRITICAL)

class R6MAPTests(unittest.TestCase):
    """Test R6 MAPs"""

    def check_section_strings(self, loadedMapFile):
        """Check all strings in the mapFile are as expected"""
        self.assertEqual(loadedMapFile.header.header_begin_message.string, "BeginMapv2.1")
        self.assertEqual(loadedMapFile.materialListHeader.material_list_string.string, "MaterialList")
        self.assertEqual(loadedMapFile.geometryListHeader.geometry_list_string.string, "GeometryList")
        self.assertEqual(loadedMapFile.portalList.section_string.string, "PortalList")
        self.assertEqual(loadedMapFile.lightList.section_string.string, "LightList")
        self.assertEqual(loadedMapFile.objectList.section_string.string, "ObjectList")
        self.assertEqual(loadedMapFile.roomList.section_string.string, "RoomList")
        self.assertEqual(loadedMapFile.planningLevelList.section_string.string, "PlanningLevelList")

        self.assertEqual(loadedMapFile.footer.end_map_string.string, "EndMap", "Unexpected end of map footer string")

    def test_R6_MAP_Structure(self):
        """Tests reading an R6 MAP file, specifically M01"""
        settings = load_settings(TEST_SETTINGS_FILE)

        map_filepath = path.join(settings["gamePath_R6_EW"], "data", "map", "m01", "M01.map")

        loadedFile = MAPLevelReader.MAPLevelFile()
        readSucessfullyToEOF = loadedFile.read_file(map_filepath)

        self.assertTrue(readSucessfullyToEOF, "Failed to read whole file")

        self.check_section_strings(loadedFile)

        self.assertEqual(loadedFile.materialListHeader.numMaterials, 263, "Unexpected number of materials")

        self.assertEqual(loadedFile.geometryListHeader.count, 57, "Unexpected number of geometry objects")

        self.assertEqual(loadedFile.portalList.portalCount, 65, "Unexpected number of portals")

        self.assertEqual(loadedFile.lightList.lightCount, 162, "Unexpected number of lights")

        self.assertEqual(loadedFile.objectList.objectCount, 38, "Unexpected number of objects")

        self.assertEqual(loadedFile.roomList.roomCount, 47, "Unexpected number of rooms")

        self.assertEqual(loadedFile.planningLevelList.planningLevelCount, 4, "Unexpected number of planning levels")


    def test_R6_MAP_Materials(self):
        """Tests reading materials from an R6 MAP file"""
        settings = load_settings(TEST_SETTINGS_FILE)

        map_filepath = path.join(settings["gamePath_R6_EW"], "data", "map", "m02", "mansion.map")

        loadedFile = MAPLevelReader.MAPLevelFile()
        loadedFile.read_file(map_filepath)

        #TODO: This is currently disabled as this file has an unread part at the end, but the rest of this test is meaninful
        #self.assertTrue(readSucessfullyToEOF, "Failed to read whole file")
        #self.check_section_strings(loadedFile)

        self.assertEqual(loadedFile.materialListHeader.numMaterials, 137, "Unexpected number of materials")

        firstMaterial = loadedFile.materials[0]
        self.assertEqual(firstMaterial.get_material_game_version(), RSEGameVersions.RAINBOW_SIX, "Wrong material format detected")
        self.assertEqual(firstMaterial.versionNumber, 1, "Wrong material version number")
        self.assertEqual(firstMaterial.material_name.string, "WI_plain5", "Wrong material name")
        self.assertEqual(firstMaterial.texture_name.string, "Wl_paper_congo_tan_leaves1.BMP", "Wrong texture name")

        self.assertAlmostEqual(firstMaterial.opacity, 1.0, 3, "Wrong opacity value")
        self.assertAlmostEqual(firstMaterial.emissiveStrength, 0.0, 3, "Wrong emissive strength value")
        self.assertEqual(firstMaterial.textureAddressMode, 3, "Wrong texture address mode value")
        self.assertEqual(firstMaterial.ambientColorUInt, [25, 25, 25], "Wrong ambient color")
        self.assertEqual(firstMaterial.diffuseColorUInt, [255, 255, 255], "Wrong diffuse color")
        self.assertEqual(firstMaterial.specularColorUInt, [229, 229, 229], "Wrong specular color")
        self.assertEqual(firstMaterial.normalizedColors, False, "Incorrectly determined whether colors are normalized in the file")
        self.assertAlmostEqual(firstMaterial.specularLevel, 0.0, 3, "Wrong specular value")
        self.assertEqual(firstMaterial.twoSided, False, "Wrong two sided material flag value")

    def test_load_all_R6_maps(self):
        """Attempt to load and validate the sections of each map in the directory"""
        settings = load_settings(TEST_SETTINGS_FILE)

        discovered_files = gather_files_in_path(".MAP", settings["gamePath_R6_EW"])

        for map_filepath in discovered_files:
            if map_filepath.endswith("obstacletest.map") or map_filepath.endswith("mansion.map") or map_filepath.endswith("m8.map") or map_filepath.endswith("m14.map"):
                #TODO: remove all of these maps, except obstacletest.map from this skip, once the last data structure is deciphered
                #I believe this is an early test map that was shipped by accident.
                # It's data structures are not consistent with the rest of the map files
                # and it is not used anywhere so it is safe to skip
                continue

            loadedFile = MAPLevelReader.MAPLevelFile()
            readSucessfullyToEOF = loadedFile.read_file(map_filepath)

            self.assertTrue(readSucessfullyToEOF, f'Failed to read whole file: {map_filepath}')

            self.check_section_strings(loadedFile)


if __name__ == '__main__':
    unittest.main()
