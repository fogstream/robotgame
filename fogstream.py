import rg


def locs_almost_around(loc):
    """
    Нахождение координат клеток, находящихся через одну от нас по
    вертикали/горизонтали.
    С этих клеток противник следующим ходом оказывается рядом с нами
    """
    x, y = loc
    offsets = ((2, 0), (0, 2), (-2, 0), (0, -2))
    result = [(x + dx, y + dy) for dx, dy in offsets]
    return result


def locs_diagonal(loc):
    """
    Нахождение координат соседних клеток, расположенных по диагонали от
    переданной клетки

    :type loc: tuple
    :rtype: list
    """
    x, y = loc
    offsets = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    result = [(x + dx, y + dy) for dx, dy in offsets]
    return result


def loc_opposite(target_loc, base_loc):
    """
    Нахождение координат клетки, расположенной напротив целевой, относительно
    базовой.

    00t   Наглядное описание действия функции:
    0b0   b - базовая клетка относительно которой ищутся координаты,
    r00   t - целевая клетка, для которой ищется противоположная клетка
          r - результирующая, координаты которой возвращаются
    """
    target_x, target_y = target_loc
    base_x, base_y = base_loc
    result_x = 2 * base_x - target_x
    result_y = 2 * base_y - target_y
    result_loc = (result_x, result_y)
    return result_loc


class Robot:
    """
    Основной класс бота. Каждый бот наследуется от него
    """
    def act(self, game):
        """
        Возвращает действие, которое совершит бот к концу раунда

        :param game: Текущее состояние игры. Отсюда можно получить информацию
                     обо всех ботах в игре

        :rtype: list
        """

        # Союзники, находящиеся на соседних клетках
        allies_adjusent = []
        # Противники, находящиеся на соседних клетках
        enemies_adjusent = []
        # Союзники, находящиеся по диагонали
        allies_diagonal = []
        # Противники, находящиеся по диагонали
        enemies_diagonal = []
        # Противники, которые следующим ходом окажутся на соседней клетке
        enemies_almost_adjusent = []

        # Определяем находится ли бот на точке респауна. Если да - уходим
        if 'spawn' in rg.loc_types(self.location):
            for loc_around in rg.locs_around(self.location):
                # Проверяем есть ли вокруг бота поля не респауны
                # Если есть - уходим туда
                if ('spawn' not in rg.loc_types(loc_around) and
                        'obstacle' not in rg.loc_types(loc_around)):
                    return ['move', loc_around]
            # Если полей не нашлось - уходим в сторону центра
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]

        # Проходимся по всем ботам, собираем информацию
        for loc, bot in game.get('robots').items():
            if bot.get('player_id') == self.player_id:
                if loc in locs_diagonal(self.location):
                    enemies_diagonal.append(bot)
                elif loc in rg.locs_around(self.location):
                    enemies_adjusent.append(bot)
                elif loc in locs_almost_around(self.location):
                    enemies_almost_adjusent.append(bot)
        if len(enemies_adjusent) > 0:
            enemy_bot = enemies_adjusent[0]
            return ['attack', enemy_bot.get('location')]
        if len(enemies_almost_adjusent) > 0:
            enemy_bot = enemies_almost_adjusent[0]
            return ['attack', rg.toward(
                self.location, enemy_bot.get('location'))]
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        # TODO: to be continued

        # Возможная стратегия для начала
        # Если вокруг есть противники:
            # Если по диагонали есть союзники
            # Если на смежной клетке с союзником есть противник - бьем его
                # ...
            # Иначе:
                # Если противников больше 1 - пробуем свалить
                # Если противник один - сравниваем хп
                    # Если у нас больше - бьем
                    # Иначе - пробуем свалить
        # Если по диагонали есть созюзники:
            # Если через одну клетку есть противник - бьем в его сторону
            # Иначе - окапываемся
        # Если вокруг никого нет
            # Если через одну клетку есть противник - бьем в его сторону
            # Иначе - идем
