sub_dict = {
    "automod.message.hold": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "automod.message.update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "automod.settings.update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "automod.terms.update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.update": {
        "version": 2,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.follow": {
        "version": 2,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.ad_break.begin": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.chat.clear": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.chat.clear_user_messages": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.chat.message": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.chat.message_delete": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.chat.notification": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.chat_settings.update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.chat.user_message_hold": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.chat.user_message_update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "user_id"
        ]},
    "channel.subscribe": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.subscription.end": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.subscription.gift": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.subscription.message": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.cheer": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.raid": {
        "version": 1,
        "conditions": [
            "from_broadcaster_user_id",
            "to_broadcaster_user_id"
        ]},
    "channel.ban": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.unban": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.unban_request.create": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.unban_request.resolve": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.moderate": {
        "version": 2,
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.moderator.add": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.moderator.remove": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.guest_star_session.begin": {
        "version": "beta",
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.guest_star_session.end": {
        "version": "beta",
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.guest_star_guest.update": {
        "version": "beta",
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.guest_star_settings.update": {
        "version": "beta",
        "conditions": [
            "broadcaster_user_id",
            "moderator_user_id"
        ]},
    "channel.channel_points_automatic_reward_redemption.add": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.channel_points_custom_reward.add": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.channel_points_custom_reward.update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "reward_id"
        ]},
    "channel.channel_points_custom_reward.remove": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "reward_id"
        ]},
    "channel.channel_points_custom_reward_redemption.add": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "reward_id"
        ]},
    "channel.channel_points_custom_reward_redemption.update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "reward_id"
        ]},
    "channel.poll.begin": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.poll.progress": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.poll.end": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.prediction.begin": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.prediction.progress": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.prediction.lock": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.prediction.end": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.suspicious_user.message": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderate_user_id"
        ]},
    "channel.suspicious_user.update": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderate_user_id"
        ]},
    "channel.vip.add": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.vip.remove": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.warning.acknowledge": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderate_user_id"
        ]},
    "channel.warning.send": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id",
            "moderate_user_id"
        ]},
    "conduit.shard.disabled": {
        "version": 1,
        "conditions": [
            "client_id",
            "conduit_id"
        ]},
    "drop.entitlement.grant": {
        "version": 1,
        "conditions": [
            "organization_id",
            "category_id",
            "campaign_id"
        ]},
    "extension.bits_transaction.create": {
        "version": 1,
        "conditions": [
            "extension_client_id"
        ]},
    "channel.goal.begin": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.goal.progress": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.goal.end": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.hype_train.begin": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.hype_train.progress": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.hype_train.end": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "channel.shield_mode.begin": {
        "version": 1,
        "conditions": []
        },
    "channel.shield_mode.end": {
        "version": 1,
        "conditions": []
        },
    "channel.shoutout.create": {
        "version": 1,
        "conditions": []
        },
    "channel.shoutout.receive": {
        "version": 1,
        "conditions": []
        },
    "stream.online": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "stream.offline": {
        "version": 1,
        "conditions": [
            "broadcaster_user_id"
        ]},
    "user.authorization.grant": {
        "version": 1,
        "conditions": [
            "client_id"
        ]},
    "user.authorization.revoke": {
        "version": 1,
        "conditions": [
            "client_id"
        ]},
    "user.update": {
        "version": 1,
        "conditions": [
            "user_id"
        ]},
    "user.whisper.message": {
        "version": 1,
        "conditions": [
            "user_id"
        ]},
}