import discord
from ..AbstractCog import AbstractCog
from discord.ext import commands
import asyncio
import re
from classes.role import Role


class Plan(AbstractCog):
    Roles = []

    def __init__(self, client):
        super().__init__(client)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Plan ready up!')

    @commands.command(name="event")
    async def prepare_event(self, ctx):

        # infos
        EventTitle = await self.textResponse(ctx, "Create New Event (Titre)", "Comment voulez-vous appelez cet event ?")
        # EventDescription = await self.textResponse(ctx, "Create New Event (Description)", "Donnez une description à l'event.")
        # EventTime = await self.textResponse(ctx, "Create New Event (Date)", "A quelle date & heure aura lieu l'event ?")
        # EventDuration = await self.textResponse(ctx, "Create New Event (Durée)", "Combien de temps dure l'event ?")


        # roles
        EventRoles = await self.role_pipeline(ctx)


        # confirm

        confirm = await self.emojiResponse(ctx, "Event",
                                           "L'evenement vous convient ? Confirmer pour poster",
                                           ["oui", "non"])
        if confirm == 0 :
            # post

            # message = EventDescription+"\n"+EventTime
            # embed = discord.Embed(title=EventTitle, description=EventDescription, colour=discord.Colour.red())
            # embed.add_field(name="Date & Heure : ", value=EventTime, inline=True)
            # embed.add_field(name="Durée : ", value=EventDuration, inline=True)
            # embed.add_field(name="Roles : ", value=EventRoles, inline=False)
            #
            # await ctx.send(embed=embed)
        else :
            self.send("Evenement annulé");

    async def role_pipeline(self, ctx):
        roleMsg = self.show_roles()
        confirmed = False
        while confirmed is not True :
            EventRoles = await self.emojiResponse(ctx, "Create New Event (Roles)", roleMsg, ["new role", "edit role", "remove role", "confirm"])
            if EventRoles == 3 :
                confirmed = True
            else :
                func = self.switcher_role(EventRoles)
                await func(ctx)

    async def new_role(self, ctx):
        RoleName = await self.textResponse(ctx, "Create New Role (Name)", "Comment voulez-vous appelez ce role ?")

        while not re.match(r'/(<a?)?:\w+:\d{18}>( \w+)+/gi', RoleName):
            RoleName = await self.textResponse(ctx, "Create New Role (Name)",
                                               "Format invalide - Comment voulez-vous appelez ce role ?");

        # split name into name & icon
            RoleEmoji = RoleName.split(" ", 1)[0]
            RoleName = RoleName.split(" ", 1)[1]


        RoleDescription = await self.textResponse(ctx, "Create New Role (Description)", "Description du role ?")
        RoleNum = await self.textResponse(ctx, "Create New Role (Number)", "Nombre de gens sur ce role ?")
        role = Role(RoleEmoji, RoleName, "RoleNum", "RoleDescription")
        self.Roles.append(role)

        await self.role_pipeline(ctx)
    async def edit_role_choice(self, ctx):
        RoleToModify = await self.emojiResponse(ctx, "Modify Role (Role)", "Quel role voulez-vous modifier ?", self.Roles)

        self.edit_role(ctx, self.Roles[RoleToModify])
    async def remove_role(self, ctx, role):
        removeRole = await self.emojiResponse(ctx, "Delete Role",
                                           "Etes-vous sur de vouloir supprimer le role : "+role.icon+" - "+role.name,
                                           ["oui", "non"])
        if removeRole == 1 :
            self.Roles.remove(role)
    async def end_role(self, ctx):
        return True

    async def edit_role(self, ctx, role):
        ModifyRole = await self.emojiResponse(ctx, "Modify Role (Property)", "Quelle propriété voulez-vous modifier ?", ["role name : "+role.name, "role description : "+role.description, "role seats : "+role.num, "end changes"])

        if ModifyRole != 3 :
            func = self.switcher_edit_role(ModifyRole)
            await func()
            await self.edit_role(ctx, role);
        self.role_pipeline(ctx);
    async def edit_rolename(self, ctx, RoleToModify):
        ModifiedName = await self.textResponse(ctx, "Modify Role (Name)", "Nouveau nom ? \n format attendu : icon rolename")
        if re.match(r'/(<a?)?:\w+:\d{18}>( \w+)+/gi', ModifiedName):
            ModifiedIcon = ModifiedName.split(" ", 1)[1]
            ModifiedName = ModifiedName.split(" ", 1)[0]

        else:
            ModifiedIcon = RoleToModify.icon
            ModifiedName = RoleToModify.name

        newName = await self.emojiResponse(ctx, "Modify Role (Name)",
                                           "Le nouveau nom : \n" + ModifiedIcon + " - " + ModifiedName + "\n, êtes vous sur ? \n celui-ci a pu ne pas etre modifier si la valeur entrée ne correspondait pas à celle attendue",
                                           ["oui", "non"])
        if newName == 0:
            self.Roles[RoleToModify].edit(name=ModifiedName, icon=ModifiedIcon)

    async def edit_roledescription(self, ctx, RoleToModify):
        ModifiedDescription = await self.textResponse(ctx, "Modify Role (Description)", "Nouvelle description ?")
        newDesc = await self.emojiResponse(ctx, "Modify Role (Name)",
                                           "La nouvelle description : \n" +ModifiedDescription+ "\n, êtes vous sur ?",
                                           ["oui", "non"])
        if newDesc == 0:
            self.Roles[RoleToModify].edit(description=ModifiedDescription)
    async def edit_rolenum(self, ctx, RoleToModify):
        ModifiedNum = await self.textResponse(ctx, "Modify Role (Seats)", "Combien de places ?")
        newNum = await self.emojiResponse(ctx, "Modify Role (Name)",
                                           "Le nombre de places : \n" + ModifiedNum + "\n, êtes vous sur ?",
                                           ["oui", "non"])
        if newNum == 0 :
            self.Roles[RoleToModify].edit(num=ModifiedNum)

    def show_roles(self):
        msg = ""
        for role in self.Roles:
            msg += role.icon + " - " + role.name + " ("+role.num+")"
            msg += "\n"
        return msg

    def switcher_role(self, argument):
        switcher = {
            0: self.new_role,
            1: self.edit_role,
            2: self.remove_role,
            3: self.end_role
        }
        func = switcher.get(argument)
        return func
    def switcher_edit_role(self, argument):
        switcher = {
            0: self.edit_rolename,
            1: self.edit_roledescription,
            2: self.edit_rolenum,
            3: self.edit_roleend
        }
        func = switcher.get(argument)
        return func


def setup(client):
    client.add_cog(Plan(client))
