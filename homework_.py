"""Версия кода с использованием Dataclass."""
from dataclasses import asdict, dataclass
from typing import ClassVar, Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    messege: ClassVar[str] = ('Тип тренировки: {0} Длительность: {1:.3f} ч.; '
                              'Дистанция: {2:.3f} км; Ср. скорость:'
                              ' {3:.3f} км/ч; Потрачено ккал: {4:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.messege.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINS_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Метод {type(self).__qualname__} в классе'
                                  f' {type(self).__name__} не определён. '
                                  f'Нужна доработка')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance,
                           speed, calories)


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_RUN_1: int = 18
    CALORIES_MEAN_SPEED_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_RUN_1 * self.get_mean_speed()
                 - self.CALORIES_MEAN_SPEED_RUN_2) * self.weight
                / self.M_IN_KM * self.duration * self.MINS_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_WALK_1: float = 0.035
    CALORIES_MEAN_SPEED_WALK_2: float = 0.029
    CALORIES_MEAN_SPEED_WALK_3: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_WALK_1 + (self.get_mean_speed()
                 ** self.CALORIES_MEAN_SPEED_WALK_3 // self.height)
                 * self.CALORIES_MEAN_SPEED_WALK_2)
                * self.weight * self.duration * self.MINS_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SWIM_1: float = 1.1
    CALORIES_MEAN_SPEED_SWIM_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SWIM_1)
                * self.CALORIES_MEAN_SPEED_SWIM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code: Dict[str, Type(Training)] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }

    if workout_type in training_code:
        return training_code[workout_type](*data)
    else:
        print('Ошибка! Попытка рассчитать данные несуществующей тренировки!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
