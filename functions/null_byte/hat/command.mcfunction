scoreboard objectives add hat trigger
scoreboard players enable @a hat
execute @a[score_hat_min=1,score_hat=1] ~ ~ ~ function null_byte:hat/equip
