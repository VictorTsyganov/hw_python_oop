class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)
        self.training_type = training_type

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

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
        self.distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = (self.action * self.LEN_STEP
                      / self.M_IN_KM) / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_min = self.duration * self.MIN_IN_H
        self.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * ((self.action * self.LEN_STEP
                          / self.M_IN_KM) / self.duration)
                         + self.CALORIES_MEAN_SPEED_SHIFT)
                         * self.weight / self.M_IN_KM * (duration_in_min))
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_min = self.duration * self.MIN_IN_H
        speed_m_in_sec = ((self.action * self.LEN_STEP / self.M_IN_KM)
                          / self.duration) * self.KMH_IN_MSEC
        self.calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                         + (speed_m_in_sec ** 2 / (self.height / self.CM_IN_M))
                         * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                         * duration_in_min)
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_SWIMMING_MULTIPLIER = 2
    CALORIES_SWIMMING_SHIFT = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.speed = (self.lenght_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        self.calories = (((self.lenght_pool * self.count_pool
                         / self.M_IN_KM / self.duration)
                         + self.CALORIES_SWIMMING_SHIFT)
                         * self.CALORIES_SWIMMING_MULTIPLIER
                         * self.weight * self.duration)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    class_training = dict_training[workout_type](*data)
    return class_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
