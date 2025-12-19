#include <iostream>
#include <string>
using namespace std;

class Character {
private:
    
    string helmetName;
    string chestName;
    string legName;
    string bootsName;

    float helmetDef;
    float chestDef;
    float legDef;
    float bootsDef;

public:

    Character(
        string hName, float hDef,
        string cName, float cDef,
        string lName, float lDef,
        string bName, float bDef
    ) {
        helmetName = hName;
        helmetDef  = hDef;

        chestName = cName;
        chestDef  = cDef;

        legName = lName;
        legDef  = lDef;

        bootsName = bName;
        bootsDef  = bDef;
    }

    void showEquipment() {
        cout << "Helmet: " << helmetName << " (" << helmetDef << " def)\n";
        cout << "Chest: " << chestName << " (" << chestDef << " def)\n";
        cout << "Legs : " << legName   << " (" << legDef   << " def)\n";
        cout << "Boots: " << bootsName << " (" << bootsDef << " def)\n";
    }
};


int main() {
    Character player(
        "Iron Helm", 5.0f,
        "Steel Armor", 12.5f,
        "Knight Leggings", 8.0f,
        "Leather Boots", 3.0f
    );

    player.showEquipment();

    return 0;
}
