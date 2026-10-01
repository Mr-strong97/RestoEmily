import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    """Remplace la PK entière par l'UUID déjà attribué à chaque compte."""

    atomic = False  # MySQL valide les ALTER TABLE hors transaction.

    dependencies = [
        ("administrateurs", "0002_administrateur_uuid"),
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("token_blacklist", "0013_alter_blacklistedtoken_options_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=[
                        # Conserver les correspondances avant de toucher aux FK.
                        "ALTER TABLE `django_admin_log` ADD COLUMN `user_uuid` UUID NULL",
                        "UPDATE `django_admin_log` AS log_entry "
                        "INNER JOIN `administrateur` AS admin_user "
                        "ON log_entry.`user_id` = admin_user.`id` "
                        "SET log_entry.`user_uuid` = admin_user.`uuid`",
                        "ALTER TABLE `token_blacklist_outstandingtoken` ADD COLUMN `user_uuid` UUID NULL",
                        "UPDATE `token_blacklist_outstandingtoken` AS token "
                        "INNER JOIN `administrateur` AS admin_user "
                        "ON token.`user_id` = admin_user.`id` "
                        "SET token.`user_uuid` = admin_user.`uuid`",
                        # Supprimer temporairement les contraintes qui visent l'ancienne PK.
                        "ALTER TABLE `django_admin_log` DROP FOREIGN KEY `django_admin_log_user_id_c564eba6_fk_administrateur_id`",
                        "ALTER TABLE `token_blacklist_outstandingtoken` DROP FOREIGN KEY `token_blacklist_outs_user_id_83bc629a_fk_administr`",
                        "ALTER TABLE `django_admin_log` DROP INDEX `django_admin_log_user_id_c564eba6_fk_administrateur_id`",
                        "ALTER TABLE `token_blacklist_outstandingtoken` DROP INDEX `token_blacklist_outs_user_id_83bc629a_fk_administr`",
                        "ALTER TABLE `django_admin_log` DROP COLUMN `user_id`",
                        "ALTER TABLE `django_admin_log` CHANGE COLUMN `user_uuid` `user_id` UUID NOT NULL",
                        "ALTER TABLE `token_blacklist_outstandingtoken` DROP COLUMN `user_id`",
                        "ALTER TABLE `token_blacklist_outstandingtoken` CHANGE COLUMN `user_uuid` `user_id` UUID NULL",
                        # uuid devient la véritable colonne id et clé primaire.
                        "ALTER TABLE `administrateur` MODIFY COLUMN `id` BIGINT NOT NULL",
                        "ALTER TABLE `administrateur` DROP PRIMARY KEY",
                        "ALTER TABLE `administrateur` CHANGE COLUMN `id` `legacy_id` BIGINT NOT NULL",
                        "ALTER TABLE `administrateur` CHANGE COLUMN `uuid` `id` UUID NOT NULL",
                        "ALTER TABLE `administrateur` ADD PRIMARY KEY (`id`)",
                        "ALTER TABLE `administrateur` DROP INDEX `administrateur_uuid_993ada44_uniq`",
                        "ALTER TABLE `administrateur` DROP COLUMN `legacy_id`",
                        # Réinstaller les références avec leur sémantique initiale.
                        "ALTER TABLE `django_admin_log` ADD INDEX `django_admin_log_user_id_c564eba6_fk_administrateur_id` (`user_id`)",
                        "ALTER TABLE `django_admin_log` ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_administrateur_id` FOREIGN KEY (`user_id`) REFERENCES `administrateur` (`id`)",
                        "ALTER TABLE `token_blacklist_outstandingtoken` ADD INDEX `token_blacklist_outs_user_id_83bc629a_fk_administr` (`user_id`)",
                        "ALTER TABLE `token_blacklist_outstandingtoken` ADD CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_administr` FOREIGN KEY (`user_id`) REFERENCES `administrateur` (`id`)",
                    ],
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name="administrateur",
                    name="uuid",
                ),
                migrations.AlterField(
                    model_name="administrateur",
                    name="id",
                    field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
            ],
        ),
    ]
