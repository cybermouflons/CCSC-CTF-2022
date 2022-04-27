#include <iostream>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <limits>
#include <numeric>
#include <cstdio>
#include <vector>
#include <string.h>
#define NAME_LEN 0x18

char placeholder[30] = "FOR FUTURE DEVELOPMENT";

enum RickType {

  EVIL_RICK,
  RICK_C137,
  PICKLE_RICK,

  UNKNOWN_TYPE,
};

static std::vector<std::string> stat_names= {"Physical attack", "Magic attack", "Physical defense",
      "Magic defense", "Speed", "Skill 1 cost", "Skill 2 cost", "Skill 3 cost",
      "Skill 4 cost"};

void rick_type_error()
{
    std::cout << "Invalid Rick type!" << std::endl;
}

RickType get_type(std::string choice)
{

  if (choice == "EvilRick") {
    return EVIL_RICK;
  }
  if (choice == "RickC137") {
    return RICK_C137;
  }
  if (choice == "PickleRick") {
    return PICKLE_RICK;
  }

  return UNKNOWN_TYPE;

}

class RickBase
{
  public:

    RickBase();
    virtual ~RickBase() {};
    virtual void change_name();
    virtual void use_ability();
    void view_stat();
    char *name;

  protected:

    long *stats;
    char **something;

};

class EvilRick : public RickBase
{
  public:

    EvilRick();
    ~EvilRick();
    void use_ability() override;
    void change_name() override;

};

class RickC137 : public RickBase
{
  public:

    RickC137();
    ~RickC137();
    void use_ability() override;

};

class PickleRick : public RickBase
{
  public:

    PickleRick();
    ~PickleRick();
    void use_ability() override;

};

RickBase::RickBase()
{
}

void RickBase::change_name()
{
  int name_len;
  std::cout << "How long is the new name? " << std::endl;
  std::cout << "> ";
  std::cin >> name_len;
  if (std::cin.fail()) {
    std::cin.clear();
  }
  std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  if (name_len < 0 || NAME_LEN - name_len < 0) {
    std::cout << "That name is too large!" << std::endl;
    return;
  }
  std::cout << "Enter new name" << std::endl;
  std::cout << "> ";
  std::cin.getline(this->name, name_len);
  if (std::cin.fail()) {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  }
}

void EvilRick::change_name()
{
  unsigned int name_len;
  std::cout << "How long is the new name? " << std::endl;
  std::cout << "> ";
  std::cin >> name_len;
  if (std::cin.fail()) {
    std::cin.clear();
  }
  std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  if (name_len < 0 || NAME_LEN - (int) name_len < 0) {
    std::cout << "That name is too large!" << std::endl;
    return;
  }
  std::cout << "Enter new name" << std::endl;
  std::cout << "> ";
  std::cin.getline(this->name, name_len);
  if (std::cin.fail()) {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  }
}


void RickBase::use_ability()
{
  std::cout << "I don't have any abilities :(" << std::endl;
}

EvilRick::EvilRick()
{
  stats = new long[stat_names.size()];
  something = new char*;
  this->name = new char[NAME_LEN];

  something[0] = placeholder;
  stats[0] = 0xab;
  stats[1] = 0x123;
  stats[2] = 0x81;
  stats[3] = 0x3f;
  stats[4] = 0x99;
  stats[5] = 0x100;
  stats[6] = 0x17;
  stats[7] = 0x2ed;
  stats[8] = 0x1;
}

EvilRick::~EvilRick() {}

void EvilRick::use_ability()
{
  std::cout << "                           _______________   ________ ________  " << std::endl;
  std::cout << "  ____  ____   ______ ____ \\_____  \\   _  \\  \\_____  \\\\_____  \\ " << std::endl;
  std::cout << "_/ ___\\/ ___\\ /  ___// ___\\ /  ____/  /_\\  \\  /  ____/ /  ____/ " << std::endl;
  std::cout << "\\  \\__\\  \\___ \\___ \\\\  \\___/       \\  \\_/   \\/       \\/       \\ " << std::endl;
  std::cout << " \\___  >___  >____  >\\___  >_______ \\_____  /\\_______ \\_______ \\" << std::endl;
  std::cout << "     \\/    \\/     \\/     \\/        \\/     \\/         \\/       \\/" << std::endl;

}

RickC137::RickC137()
{
  stats = new long[stat_names.size()];
  something = new char*;
  this->name = new char[NAME_LEN];

  something[0] = placeholder;
  stats[0] = 0x28;
  stats[1] = 0x77;
  stats[2] = 0x11;
  stats[3] = 0xad;
  stats[4] = 0xef;
  stats[5] = 0x88;
  stats[6] = 0x2;
  stats[7] = 0x12;
  stats[8] = 0xee;
}

RickC137::~RickC137() {}

void RickC137::use_ability()
{

  std::system(this->name);

}


PickleRick::PickleRick()
{
  stats = new long[6];
  something = new char*;
  this->name = new char[NAME_LEN];

  something[0] = placeholder;
  stats[0] = 0x15;
  stats[1] = 0xcc;
  stats[2] = 0x30;
  stats[3] = 0x77;
  stats[4] = 0x11;
  stats[5] = 0xce;

}

PickleRick::~PickleRick() {}

void PickleRick::use_ability()
{
  std::cout << "                                                ░░████████████                  " << std::endl;
  std::cout << "                                              ████▒▒▒▒▒▒▒▒▒▒▒▒████              " << std::endl;
  std::cout << "                                          ░░██▒▒░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒██▓▓          " << std::endl;
  std::cout << "                                          ██▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓        " << std::endl;
  std::cout << "                                        ██▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓      " << std::endl;
  std::cout << "                                      ██▒▒░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓    " << std::endl;
  std::cout << "                                    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▓▓    " << std::endl;
  std::cout << "                                    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▓▓  " << std::endl;
  std::cout << "                                  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▓▓  " << std::endl;
  std::cout << "                                  ██▒▒▒▒▒▒▒▒░░░░░░░░░░▒▒▒▒▒▒░░░░░░░░░░▒▒▒▒▒▒▓▓  " << std::endl;
  std::cout << "                                  ██▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░▒▒▒▒░░░░░░▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                                ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                                ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                                ██▒▒▒▒▒▒        ░░░░░░░░░░░░▒▒▒▒░░░░░░▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                                ██▒▒▒▒          ▒▒░░░░░░░░░░░░░░▒▒▒▒░░▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                              ██▒▒▒▒              ▒▒░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                              ██▒▒▒▒      ▒▒      ▒▒░░░░░░      ▒▒░░░░▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                              ██▒▒▒▒              ▒▒░░░░          ▒▒▒▒▒▒▒▒▒▒▒▒██" << std::endl;
  std::cout << "                            ██▒▒▒▒▒▒▒▒            ▒▒░░              ▒▒▒▒▒▒▒▒▓▓  " << std::endl;
  std::cout << "                            ██▒▒▒▒▒▒▒▒▒▒        ░░░░░░      ▓▓      ▒▒▒▒▒▒▒▒▓▓  " << std::endl;
  std::cout << "                            ██▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒░░░░░░░░              ▒▒▒▒▒▒▒▒▓▓  " << std::endl;
  std::cout << "                          ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░▒▒░░░░░░            ▒▒▒▒▒▒▒▒▓▓  " << std::endl;
  std::cout << "                          ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒░░░░░░░░          ▒▒▒▒▒▒▒▒▓▓    " << std::endl;
  std::cout << "                          ██▒▒▒▒▒▒▒▒▓▓▓▓  ░░░░▒▒░░▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓    " << std::endl;
  std::cout << "                        ▓▓▓▓▒▒▒▒▒▒▓▓████▓▓░░▒▒▒▒▒▒░░░░▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓    " << std::endl;
  std::cout << "                        ██▒▒▒▒▒▒▒▒████████▒▒░░░░▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓    " << std::endl;
  std::cout << "                        ██▒▒▒▒▒▒▒▒██████████▓▓▒▒░░    ▒▒    ▓▓▒▒▒▒▒▒▒▒▒▒▓▓      " << std::endl;
  std::cout << "                      ▓▓▓▓▒▒▒▒▒▒▒▒██████████████▓▓▓▓████▓▓████▓▓▒▒▒▒▒▒▒▒▓▓      " << std::endl;
  std::cout << "                      ██▒▒▒▒▒▒▒▒▒▒▒▒  ████▓▓▒▒▒▒████████████████▒▒▒▒▒▒▒▒▓▓      " << std::endl;
  std::cout << "                      ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ██▓▓▒▒▒▒▒▒████████████▒▒▒▒▒▒▒▒██      " << std::endl;
  std::cout << "                    ██▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ░░▓▓▒▒▒▒▒▒████████▒▒▒▒▒▒▒▒▓▓        " << std::endl;
  std::cout << "                    ██▒▒░░▒▒▒▒▒▒▒▒░░░░░░░░▒▒░░    ▒▒    ██▒▒▒▒▒▒▒▒▒▒▒▒▓▓        " << std::endl;
  std::cout << "                    ██▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓        " << std::endl;
  std::cout << "                  ██▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓        " << std::endl;
  std::cout << "                  ██▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓          " << std::endl;
  std::cout << "                ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓          " << std::endl;
  std::cout << "                ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓          " << std::endl;
  std::cout << "              ▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓            " << std::endl;
  std::cout << "              ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓            " << std::endl;
  std::cout << "            ██▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██              " << std::endl;
  std::cout << "            ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██              " << std::endl;
  std::cout << "          ▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                " << std::endl;
  std::cout << "          ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒▒▒██                " << std::endl;
  std::cout << "        ██▓▓▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒▓▓░░                " << std::endl;
  std::cout << "        ██▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒▒▒██                  " << std::endl;
  std::cout << "      ▒▒▓▓▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░░                  " << std::endl;
  std::cout << "      ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                    " << std::endl;
  std::cout << "    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                      " << std::endl;
  std::cout << "    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                      " << std::endl;
  std::cout << "    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓░░                      " << std::endl;
  std::cout << "    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓                        " << std::endl;
  std::cout << "  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                          " << std::endl;
  std::cout << "  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                          " << std::endl;
  std::cout << "  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                            " << std::endl;
  std::cout << "  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒██                            " << std::endl;
  std::cout << "  ██▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒██                              " << std::endl;
  std::cout << "  ██▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓                                " << std::endl;
  std::cout << "  ██░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓██                                  " << std::endl;
  std::cout << "  ██▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒██                                    " << std::endl;
  std::cout << "    ██░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒██                                      " << std::endl;
  std::cout << "    ██▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                                        " << std::endl;
  std::cout << "      ██▒▒░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                                          " << std::endl;
  std::cout << "        ██▒▒░░░░░░░░░░░░░░▒▒▒▒▒▒████                                            " << std::endl;
  std::cout << "          ██████▒▒░░░░░░░░██████                                                " << std::endl;
  std::cout << "                ██████████                                                      " << std::endl;
  std::cout << std::flush;
}

void RickBase::view_stat()
{
  std::string stat_name;
  int idx;

  std::cout << "Which stat do you want to see? (";
  std::string s = std::accumulate(std::begin(stat_names), std::end(stat_names), std::string(),
                                  [](std::string &ss, std::string &s)
                                  {
                                      return ss.empty() ? s : ss + ", " + s;
                                  });
  std::cout << s;

  std::cout << ")";

  std::cout << "> ";
  std::getline(std::cin, stat_name);
  if (std::cin.fail()) {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  }

  auto it = std::find(stat_names.begin(), stat_names.end(), stat_name);
  if (it != stat_names.end()) {
    idx = it - stat_names.begin();
    std::cout << stat_name << ": " << this->stats[idx] << std::endl;
  } else {
    std::cout << "No such stat!" << std::endl;
  }

}

RickBase *createRick()
{
  std::string rick_class;
  RickBase *obj;
  RickType rick_type;

  std::cout << "Choose Rick class" << std::endl;
  std::cout << "> ";
  std::getline(std::cin, rick_class);
  if (std::cin.fail()) {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  }

  rick_type = get_type(rick_class);

  switch (rick_type) {
    default:
    case UNKNOWN_TYPE:
      rick_type_error();
      return nullptr;
    case EVIL_RICK:
      obj = new EvilRick();
      break;
    case RICK_C137:
      obj = new RickC137();
      std::cout << "You haven't unlocked this Rick yet!" << std::endl;
      delete obj;
      return nullptr;
    case PICKLE_RICK:
      obj = new PickleRick();
      break;
  };

  std::cout << "Choose Rick name" << std::endl;
  std::cout << "> ";
  std::cin.getline(obj->name, NAME_LEN);
  if (std::cin.fail()) {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
  }

  return obj;
}

RickBase *choose_rick(RickBase *own, RickBase *enemy) {
  int rick_choice = 0;
  std::cout << "For which Rick?" << std::endl;
  while (!(rick_choice == 1 || rick_choice == 2)) {
    std::cout << "[1] Your own" << std::endl;
    std::cout << "[2] The opponent's" << std::endl;
    std::cout << "> ";
    std::cin >> rick_choice;
    if (std::cin.fail()) {
      std::cin.clear();
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    if (!(rick_choice == 1 || rick_choice == 2)) {
      std::cout << "Bad choice!" << std::endl;
    }
  }
  if (rick_choice == 1) {
    return own;
  } else {
    return enemy;
  }
}

void print_menu()
{
    std::cout << "[1] View one of your Rick's stats" << std::endl;
    std::cout << "[2] Change a Rick's name" << std::endl;
    std::cout << "[3] Begin battle!" << std::endl;
}

void prepare_for_battle(RickBase *rick, RickBase *enemy)
{
  int choice = 0;
  RickBase *char_choice;
  std::cout << "Any last changes before battle begins?" << std::endl;
  while (choice != 3)
  {
    print_menu();
    std::cout << "Choice" << std::endl;
    std::cout << "> ";
    std::cin >> choice;
    if (std::cin.fail()) {
      std::cin.clear();
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    switch (choice) {
      case 1:
        char_choice = choose_rick(rick, enemy);
        char_choice->view_stat();
        break;
      case 2:
        char_choice = choose_rick(rick, enemy);
        char_choice->change_name();
        break;
      default:
        std::cout << "Bad choice!" << std::endl;
        break;
    }
  }
}

int main()
{

  RickBase *hero = nullptr;
  RickBase *enemy = nullptr;

  std::cout << "Create your Rick: " << std::endl;
  do {
    hero = createRick();
  } while (!hero);

  std::cout << "Choose your opponent's Rick:" << std::endl;
  do{
    enemy = createRick();
  } while (!enemy);


  prepare_for_battle(hero, enemy);

  std::cout << hero->name << ", attack!" << std::endl;
  hero->use_ability();
  std::cout << enemy->name << ", attack!" << std::endl;
  enemy->use_ability();

  return 0;
}
